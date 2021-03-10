import time
from datetime import datetime

from _datetime import timedelta
from sqlalchemy import and_, update
from typing import List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from mapadroid.db.model import TrsSpawn
from mapadroid.geofence.geofenceHelper import GeofenceHelper
from mapadroid.utils.collections import Location
from mapadroid.utils.logging import LoggerEnums, get_logger

logger = get_logger(LoggerEnums.database)


# noinspection PyComparisonWithNone
class TrsSpawnHelper:
    @staticmethod
    async def get(session: AsyncSession, spawn_id: int) -> Optional[TrsSpawn]:
        stmt = select(TrsSpawn).where(TrsSpawn.spawnpoint == spawn_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_all(session: AsyncSession, spawn_ids: List[int] = None) -> List[TrsSpawn]:
        stmt = select(TrsSpawn)
        if spawn_ids is not None:
            stmt = stmt.where(TrsSpawn.spawnpoint.in_(spawn_ids))
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def __get_of_area(session: AsyncSession, geofence_helper: GeofenceHelper,
                            additional_event: Optional[int], only_unknown_endtime: bool = False) -> List[TrsSpawn]:
        if not geofence_helper:
            logger.warning("No geofence helper was passed. Returning empty list of spawns.")
            return []
        min_lat, min_lon, max_lat, max_lon = geofence_helper.get_polygon_from_fence()
        event_ids: list = [1]
        if additional_event is not None:
            event_ids.append(additional_event)

        where_condition = and_(TrsSpawn.eventid.in_(event_ids),
                               TrsSpawn.latitude >= min_lat,
                               TrsSpawn.longitude >= min_lon,
                               TrsSpawn.latitude <= max_lat,
                               TrsSpawn.longitude <= max_lon)
        if only_unknown_endtime:
            where_condition = and_(TrsSpawn.calc_endminsec == None, where_condition)

        stmt = select(TrsSpawn).where(where_condition)
        result = await session.execute(stmt)
        list_of_spawns: List[TrsSpawn] = []
        for spawnpoint in result:
            if not geofence_helper.is_coord_inside_include_geofence([spawnpoint.latitude, spawnpoint.longitude]):
                continue
            list_of_spawns.append(spawnpoint)
        return list_of_spawns

    @staticmethod
    async def get_known_of_area(session: AsyncSession, geofence_helper: GeofenceHelper,
                                additional_event: Optional[int]) -> List[TrsSpawn]:
        """
        Used to be DbWrapper::get_detected_spawns.
        Fetches any spawnpoint in the given area defined by geofence_helper
        Args:
            session:
            geofence_helper:
            additional_event:

        Returns: List of spawnpoints in the area (both with known and unknown despawn time)
        """
        return await TrsSpawnHelper.__get_of_area(session, geofence_helper, additional_event)

    @staticmethod
    async def get_known_without_despawn_of_area(session: AsyncSession, geofence_helper: GeofenceHelper,
                                                additional_event: Optional[int]) -> List[TrsSpawn]:
        """
        Used to be DbWrapper::get_undetected_spawns.
        Fetches any spawnpoint in the given area defined by geofence_helper
        Args:
            session:
            geofence_helper:
            additional_event:

        Returns: List of spawnpoints in the area (with unknown despawn time)
        """
        return await TrsSpawnHelper.__get_of_area(session, geofence_helper, additional_event, only_unknown_endtime=True)

    @staticmethod
    async def convert_spawnpoints(session: AsyncSession, spawnpoint_ids: List[int], event_id: int = 1) -> None:
        stmt = update(TrsSpawn).where(TrsSpawn.spawnpoint.in_(spawnpoint_ids)).values(eventid=event_id)
        await session.execute(stmt)

    @staticmethod
    async def get_next_spawns(session: AsyncSession, geofence_helper: GeofenceHelper,
                              additional_event: Optional[int]) -> List[Tuple[int, Location]]:
        """
        Used to be DbWrapper::retrieve_next_spawns
        Fetches the spawnpoints of which the calculated spawn time is upcoming within the next hour and converts it
        to a List of tuples consisting of (timestamp of spawn, Location)
        Args:
            session:
            geofence_helper:
            additional_event:

        Returns:

        """
        if not geofence_helper:
            logger.warning("No geofence helper was passed. Returning empty list of spawns.")
            return []
        min_lat, min_lon, max_lat, max_lon = geofence_helper.get_polygon_from_fence()
        event_ids: list = [1]
        if additional_event is not None:
            event_ids.append(additional_event)

        stmt = select(TrsSpawn).where(and_(TrsSpawn.eventid.in_(event_ids),
                               TrsSpawn.latitude >= min_lat,
                               TrsSpawn.longitude >= min_lon,
                               TrsSpawn.latitude <= max_lat,
                               TrsSpawn.longitude <= max_lon,
                               TrsSpawn.calc_endminsec != None))
        result = await session.execute(stmt)
        next_up: List[Tuple[int, Location]] = []
        current_time = time.time()
        current_time_of_day = datetime.now().replace(microsecond=0)
        timedelta_to_be_added = timedelta(hours=1)
        for spawn in result:
            if not geofence_helper.is_coord_inside_include_geofence([spawn.latitude, spawn.longitude]):
                continue
            endminsec_split = spawn.calc_endminsec.split(":")
            minutes = int(endminsec_split[0])
            seconds = int(endminsec_split[1])
            temp_date = current_time_of_day.replace(
                minute=minutes, second=seconds)
            if minutes < current_time_of_day.minute:
                # Add an hour to have the next spawn at the following hour respectively
                temp_date = temp_date + timedelta_to_be_added

            if temp_date < current_time_of_day:
                # spawn has already happened, we should've added it in the past, let's move on
                # TODO: consider crosschecking against current mons...
                continue
            spawn_duration_minutes = 60 if spawn.spawndef == 15 else 30

            timestamp = time.mktime(temp_date.timetuple()) - spawn_duration_minutes * 60
            # check if we calculated a time in the past, if so, add an hour to it...
            timestamp = timestamp + 60 * 60 if timestamp < current_time else timestamp
            next_up.append((int(timestamp), Location(spawn.latitude, spawn.longitude)))
        return next_up