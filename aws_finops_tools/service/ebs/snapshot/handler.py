from typing import List, Dict, Any, Optional, Union, TypedDict
import asyncio
import aioboto3
from ....interfaces.service_interface import ServiceInterface

class SnapshotInfo(TypedDict):
    """EBS snapshot information type definition"""
    id: str
    volume_id: str
    state: str
    progress: str
    start_time: str
    size: int
    description: str
    encrypted: bool
    region: str

class SnapshotHandler(ServiceInterface[SnapshotInfo]):
    """Handler for EBS snapshot operations"""
    
    async def fetch_data(self) -> List[SnapshotInfo]:
        """Fetch EBS snapshot data asynchronously"""
        async with aioboto3.Session(**self.session_args).client("ec2", region_name=self.region) as ec2:
            try:
                response = await ec2.describe_snapshots(OwnerIds=["self"])
                snapshots = response.get("Snapshots", [])
                
                result = []
                for snap in snapshots:
                    result.append({
                        "id": snap["SnapshotId"],
                        "volume_id": snap.get("VolumeId", ""),
                        "state": snap["State"],
                        "progress": snap["Progress"],
                        "start_time": snap["StartTime"].strftime("%Y-%m-%d %H:%M:%S"),
                        "size": snap.get("VolumeSize", 0),
                        "description": snap.get("Description", ""),
                        "encrypted": snap.get("Encrypted", False),
                        "region": self.region
                    })
                
                return result
            except Exception as e:
                print(f"Failed to fetch EBS snapshots: {e}")
                return []

