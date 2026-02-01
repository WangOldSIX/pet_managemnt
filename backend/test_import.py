#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test imports"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    print("Step 1: Import config...")
    from app.core.config import settings
    print("OK: config imported")
    print(f"  APP_NAME: {settings.APP_NAME}")
except Exception as e:
    print(f"FAIL: config failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nStep 2: Import response...")
    from app.core.response import ApiResponse, TokenResponse, PageResponse
    print("OK: response imported")
except Exception as e:
    print(f"FAIL: response failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nStep 3: Import database...")
    from app.core.database import engine, Base, get_db
    print("OK: database imported")
except Exception as e:
    print(f"FAIL: database failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nStep 4: Import schemas...")
    from app.schemas import UserCreate, UserResponse, PetCreate, PetResponse
    print("OK: schemas imported")
except Exception as e:
    print(f"FAIL: schemas failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nStep 5: Import models...")
    from app.db.models import User, Pet, Service, Order
    print("OK: models imported")
except Exception as e:
    print(f"FAIL: models failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nStep 6: Import crud...")
    from app.crud import get_user, get_pet, create_order
    print("OK: crud imported")
except Exception as e:
    print(f"FAIL: crud failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nStep 7: Import service...")
    from app.service import UserService, PetService, OrderService
    print("OK: service imported")
except Exception as e:
    print(f"FAIL: service failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nStep 8: Import security...")
    from app.core.security import create_access_token, verify_password
    print("OK: security imported")
except Exception as e:
    print(f"FAIL: security failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nStep 9: Import exceptions...")
    from app.core.exceptions import BusinessException, NotFoundError
    print("OK: exceptions imported")
except Exception as e:
    print(f"FAIL: exceptions failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nStep 10: Import deps...")
    from app.core.deps import get_current_user, require_admin
    print("OK: deps imported")
except Exception as e:
    print(f"FAIL: deps failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nStep 11: Import api modules...")
    from app.api import auth, users, dashboard
    print("OK: api modules imported")
except Exception as e:
    print(f"FAIL: api modules failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nStep 12: Import main...")
    from app.main import app
    print("OK: main imported")
    print(f"  App title: {app.title}")
    print(f"  App version: {app.version}")
except Exception as e:
    print(f"FAIL: main failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("Import test completed!")
print("="*50)
