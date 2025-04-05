from typing import List, Dict, Any, Optional, Union, TypedDict
import aioboto3
from ....interfaces.service_interface import ServiceInterface


class VolumeInfo(TypedDict):
    """EBS volume information type definition"""
    id: str
    size: int
    type: str
    state: str
    created: str
    encrypted: bool
    availability_zone: str
    attachments: List[Dict[str, Any]]
    region: str


class VolumeHandler(ServiceInterface[VolumeInfo]):
    """Handler for EBS volume operations"""
    
    async def fetch_data(self) -> List[VolumeInfo]:
        """Fetch EBS volume data asynchronously"""
        async with aioboto3.Session(**self.session_args).client("ec2", region_name=self.region) as ec2:
            try:
                response = await ec2.describe_volumes()
                volumes = response.get("Volumes", [])
                
                result = []
                for vol in volumes:
                    result.append({
                        "id": vol["VolumeId"],
                        "size": vol["Size"],
                        "type": vol["VolumeType"],
                        "state": vol["State"],
                        "created": vol["CreateTime"].strftime("%Y-%m-%d %H:%M:%S"),
                        "encrypted": vol["Encrypted"],
                        "availability_zone": vol["AvailabilityZone"],
                        "attachments": vol.get("Attachments", []),
                        "region": self.region
                    })
                
                return result
            except Exception as e:
                print(f"Failed to fetch EBS volumes: {e}")
                return []
    
    async def fetch_unused_volumes(self) -> List<VolumeInfo]:
        """Fetch unused EBS volume data asynchronously"""
        async with aioboto3.Session(**self.session_args).client("ec2", region_name=self.region) as ec2:
            try:
                response = await ec2.describe_volumes(
                    Filters=[{"Name": "status", "Values": ["available"]}]
                )
                volumes = response.get("Volumes", [])
                
                result = []
                for vol in volumes:
                    result.append({
                        "id": vol["VolumeId"],
                        "size": vol["Size"],
                        "type": vol["VolumeType"],
                        "state": vol["State"],
                        "created": vol["CreateTime"].strftime("%Y-%m-%d %H:%M:%S"),
                        "encrypted": vol["Encrypted"],
                        "availability_zone": vol["AvailabilityZone"],
                        "attachments": vol.get("Attachments", []),
                        "region": self.region
                    })
                
                return result
            except Exception as e:
                print(f"Failed to fetch unused EBS volumes: {e}")
                return []
