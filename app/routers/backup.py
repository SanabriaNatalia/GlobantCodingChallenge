"""This module contains the backup and restore endpoints for the API."""

from fastapi import APIRouter, Depends, HTTPException, status
from utils.backup.backup_db import backup_table
from database.database_config import get_db

router = APIRouter(
    prefix="/backup",
    tags=["backup"],
    responses={404: {"description": "Not found"}},
)

@router.post("/backup/{table_name}")
def create_backup(table_name: str):
    """Endpoint to trigger a backup of a specific table."""
    try:
        message = backup_table(table_name)
        return {"status": "success", "message": message}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/restore/{table_name}")
def restore_backup(table_name: str):
    """Endpoint to restore a specific table from a backup."""
    try:
        message = restore_table_from_backup(table_name)
        return {"status": "success", "message": message}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")