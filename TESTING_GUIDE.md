# Testing Guide - flaer Data Center Onboarding

Complete guide for testing the data center onboarding and tracking system.

---

## Quick Start Testing

### 1. Start the Application

```bash
# Terminal 1 - Backend
cd flaer/backend
DATABASE_URL="postgresql+psycopg://localhost/flaer" venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000

# Terminal 2 - Frontend
cd flaer/frontend-svelte
npm run dev
```

Backend runs on: `http://localhost:8000`  
Frontend runs on: `http://localhost:5173`

---

## Test Scenarios

### Scenario 1: New User Registration & First Data Center

#### Step 1: Register Account
1. Navigate to `http://localhost:5173`
2. Click **"Get Started"** or **"Sign Up"**
3. Fill in registration form:
   - Full Name: `Test User`
   - Email: `test@example.com`
   - Password: `SecurePass123!`
   - Company: `Test Data Centers Inc`
4. Click **"Create Account"**
5. ✅ **Expected**: Redirected to dashboard with empty state

#### Step 2: Add First Data Center
1. In dashboard, click **"+ Add Data Center"** button
2. **Step 1 - Basic Info**:
   - Name: `Virginia DC-1`
   - Location: `Ashburn, Virginia, USA`
   - Latitude: `38.9072`
   - Longitude: `-77.0369`
   - Click **"Next"**
3. **Step 2 - Metrics**:
   - Capacity: `150` MW
   - PUE: `1.42` (should show "Fair" badge in amber)
   - Carbon Intensity: `412` gCO2/kWh (should show "High" badge in red)
   - Renewable %: Slide to `48%`
   - Click **"Next"**
4. **Step 3 - Optional**:
   - WUE: `1.8` L/kWh
   - CUE: `0.58`
   - Skip monitoring integration (disabled)
   - Click **"Add Data Center"**
5. ✅ **Expected**: 
   - Success screen appears
   - After 1.5 seconds, modal closes
   - Data center appears in portfolio view
   - Map shows marker at Virginia location

#### Step 3: Verify Calculations
1. Check the data center card shows:
   - Risk Level: **Medium** or **High** (PUE 1.42, Carbon 412)
   - Annual CO2: ~**124K tCO₂e**
   - Annual Water: ~**2.4M m³**
   - Forecast 2035: **+5%** to **+15%**
   - CSRD Exposure: **Medium** or **Low**

---

### Scenario 2: Add Multiple Data Centers

#### Add Stockholm (Best Practice Example)
1. Click **"+ Add Data Center"**
2. Fill in:
   - Name: `Stockholm DC`
   - Location: `Stockholm, Sweden`
   - Capacity: `200` MW
   - PUE: `1.08` (should show "Excellent" badge in green)
   - Carbon Intensity: `22` gCO2/kWh (should show "Very Low" badge in green)
   - Renewable %: `98%`
   - WUE: `0.4` L/kWh
3. ✅ **Expected**:
   - Risk Level: **Low**
   - Annual CO2: ~**8K tCO₂e** (very low)
   - Forecast 2035: **-25%** (improving)
   - CSRD Exposure: **Low**

#### Add Singapore (High Risk Example)
1. Click **"+ Add Data Center"**
2. Fill in:
   - Name: `Singapore DC`
   - Location: `Singapore`
   - Capacity: `120` MW
   - PUE: `1.38`
   - Carbon Intensity: `408` gCO2/kWh
   - Renewable %: `35%`
   - WUE: `2.1` L/kWh
3. ✅ **Expected**:
   - Risk Level: **High**
   - Annual CO2: ~**98K tCO₂e**
   - Forecast 2035: **+12%**
   - CSRD Exposure: **Medium**

#### Verify Portfolio Summary
1. Check portfolio statistics update:
   - Total Facilities: **3**
   - Total Capacity: **470 MW**
   - Avg PUE: ~**1.29** (capacity-weighted)
   - Avg Carbon Intensity: ~**147 gCO2/kWh**
   - Avg Renewable: ~**60%**
   - Risk Breakdown: High: 1, Medium: 1, Low: 1

---

### Scenario 3: API Testing with curl

#### Get Auth Token
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "api-test@example.com",
    "password": "SecurePass123!",
    "full_name": "API Test User",
    "company": "API Test Co"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "api-test@example.com",
    "password": "SecurePass123!"
  }'

# Save the token from response
TOKEN="your_token_here"
```

#### Create Data Center via API
```bash
curl -X POST http://localhost:8000/api/data-centers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Frankfurt DC",
    "location": "Frankfurt, Germany",
    "latitude": 50.1109,
    "longitude": 8.6821,
    "capacity_mw": 180,
    "pue": 1.24,
    "wue": 1.2,
    "cue": 0.35,
    "carbon_intensity": 284,
    "renewable_pct": 72
  }'
```

✅ **Expected Response**:
```json
{
  "id": "uuid-here",
  "organization_id": "org-uuid",
  "name": "Frankfurt DC",
  "location": "Frankfurt, Germany",
  "capacity_mw": 180,
  "pue": 1.24,
  "carbon_intensity": 284,
  "renewable_pct": 72,
  "risk_level": "low",
  "annual_co2": "76K tCO₂e",
  "annual_water": "1.2M m³",
  "forecast_2035": "-15%",
  "csrd_exposure": "High",
  "is_active": true,
  "created_at": "2026-05-07T13:48:00Z",
  "updated_at": "2026-05-07T13:48:00Z"
}
```

#### List All Data Centers
```bash
curl -X GET http://localhost:8000/api/data-centers \
  -H "Authorization: Bearer $TOKEN"
```

#### Get Portfolio Summary
```bash
curl -X GET http://localhost:8000/api/data-centers/summary \
  -H "Authorization: Bearer $TOKEN"
```

#### Update Data Center Metrics
```bash
curl -X PUT http://localhost:8000/api/data-centers/{dc_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "pue": 1.20,
    "renewable_pct": 75,
    "carbon_intensity": 270
  }'
```

✅ **Expected**: Risk level recalculated, annual metrics updated

#### Delete Data Center
```bash
curl -X DELETE http://localhost:8000/api/data-centers/{dc_id} \
  -H "Authorization: Bearer $TOKEN"
```

✅ **Expected**: `{"message": "Data center deactivated successfully"}`

---

### Scenario 4: Validation Testing

#### Test PUE Validation
1. Try to add data center with PUE = `0.9`
   - ✅ **Expected**: Error "PUE cannot be less than 1.0"
2. Try PUE = `2.6`
   - ✅ **Expected**: Error "PUE above 2.5 indicates severe inefficiency"
3. Try PUE = `1.5`
   - ✅ **Expected**: Accepted, shows "Good" badge

#### Test Carbon Intensity Validation
1. Try carbon intensity = `-10`
   - ✅ **Expected**: Error "must be between 0 and 1000"
2. Try carbon intensity = `1500`
   - ✅ **Expected**: Error "must be between 0 and 1000"
3. Try carbon intensity = `300`
   - ✅ **Expected**: Accepted, shows "Medium" badge

#### Test Renewable Percentage
1. Try renewable % = `150`
   - ✅ **Expected**: Error "must be between 0 and 100"
2. Try renewable % = `-5`
   - ✅ **Expected**: Error "must be between 0 and 100"
3. Try renewable % = `80`
   - ✅ **Expected**: Accepted

#### Test Required Fields
1. Leave name empty, click Next
   - ✅ **Expected**: Error "Data center name is required"
2. Leave location empty, click Next
   - ✅ **Expected**: Error "Location is required"

---

### Scenario 5: Plan Limits Testing

#### Test Free Tier Limit (3 Data Centers)
1. Add 3 data centers successfully
2. Try to add 4th data center
3. ✅ **Expected**: Error message:
   ```
   Data center limit reached. Your plan allows 3 facilities. 
   Upgrade to add more.
   ```

#### Test API Rate Limiting
1. Make 25 rapid POST requests to `/api/data-centers`
2. ✅ **Expected**: After 20 requests, receive `429 Too Many Requests`

---

### Scenario 6: AI Assistant Integration

#### Test Context Detection
1. With 0 data centers:
   - Open AI Assistant
   - ✅ **Expected**: Shows "Planning" conversation starters
   - Ask: "Where should I build my data center?"
   - ✅ **Expected**: AI recommends locations with scoring

2. With 1+ data centers:
   - Open AI Assistant
   - ✅ **Expected**: Shows "Operator" conversation starters
   - Ask: "Generate my weekly digest"
   - ✅ **Expected**: AI provides consumption summary with your data

#### Test Anomaly Detection
1. Add data center with PUE = `1.8`
2. Ask AI: "Check for anomalies"
3. ✅ **Expected**: AI flags "PUE above 1.75 threshold"

---

### Scenario 7: Real-time Updates

#### Test Metric Updates
1. Add data center with PUE = `1.5`, Renewable = `50%`
2. Note the risk level (likely "Medium")
3. Update via API or UI:
   - PUE → `1.2`
   - Renewable → `80%`
4. ✅ **Expected**:
   - Risk level changes to "Low"
   - Annual CO2 decreases
   - Forecast 2035 improves (more negative %)
   - Card color changes from amber to green

---

## Browser Testing

### Supported Browsers
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Responsive Testing
1. Desktop (1920x1080): Full layout with sidebar
2. Tablet (768x1024): Responsive grid, collapsible sidebar
3. Mobile (375x667): Stacked layout, hamburger menu

---

## Performance Testing

### Load Testing
```bash
# Install Apache Bench
brew install httpd  # macOS
apt-get install apache2-utils  # Linux

# Test data center creation endpoint
ab -n 100 -c 10 -H "Authorization: Bearer $TOKEN" \
   -p datacenter.json -T application/json \
   http://localhost:8000/api/data-centers
```

✅ **Expected**: 
- 95% of requests < 200ms
- 0% error rate
- Throughput > 50 req/sec

---

## Database Testing

### Verify Data Persistence
```bash
# Connect to SQLite database
sqlite3 flaer/backend/flaer.db

# Check data centers table
SELECT * FROM data_centers;

# Check organization limits
SELECT name, max_data_centers, plan_tier FROM organizations;

# Check audit logs
SELECT * FROM audit_logs WHERE resource_type = 'data_center';
```

---

## Error Handling Testing

### Test Network Errors
1. Stop backend server
2. Try to add data center in UI
3. ✅ **Expected**: Error message "Failed to create data center"

### Test Invalid Token
```bash
curl -X GET http://localhost:8000/api/data-centers \
  -H "Authorization: Bearer invalid_token"
```
✅ **Expected**: `401 Unauthorized`

### Test Missing Fields
```bash
curl -X POST http://localhost:8000/api/data-centers \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test"}'
```
✅ **Expected**: `422 Validation Error` with field details

---

## Automated Testing

### Backend Unit Tests
```bash
cd flaer/backend
pytest tests/test_data_center_service.py -v
```

### Frontend Component Tests
```bash
cd flaer/frontend-svelte
npm run test
```

### E2E Tests with Playwright
```bash
cd flaer/frontend-svelte
npx playwright test
```

---

## Checklist

### Backend ✅
- [ ] Data center CRUD operations work
- [ ] Automatic calculations are correct
- [ ] Risk level algorithm works
- [ ] Plan limits enforced
- [ ] Rate limiting active
- [ ] Authentication required
- [ ] Organization isolation works
- [ ] Audit logs created

### Frontend ✅
- [ ] Add Data Center wizard opens
- [ ] 3-step form navigation works
- [ ] Validation shows errors
- [ ] Success screen appears
- [ ] Data center appears in portfolio
- [ ] Map markers render correctly
- [ ] Portfolio summary updates
- [ ] Responsive on mobile

### Integration ✅
- [ ] AI Assistant detects context
- [ ] Weekly digests use real data
- [ ] Anomaly detection works
- [ ] Site IQ recommendations accurate
- [ ] Dashboard mode switching works

---

## Common Issues & Solutions

### Issue: "Module not found" errors
**Solution**: 
```bash
cd flaer/backend
pip install -r requirements.txt
```

### Issue: Database not initialized
**Solution**:
```bash
cd flaer/backend
python init_database.py
```

### Issue: CORS errors in browser
**Solution**: Check `main.py` CORS settings include `http://localhost:5173`

### Issue: Map not rendering
**Solution**: Check Mapbox token in environment variables

### Issue: Rate limit hit during testing
**Solution**: Wait 1 minute or restart backend to reset counters

---

## Success Criteria

✅ **System is working correctly if:**
1. User can register and login
2. User can add data center through 3-step wizard
3. Data center appears in portfolio with correct calculations
4. Risk level is calculated accurately
5. Portfolio summary updates correctly
6. API endpoints return expected responses
7. Validation prevents invalid data
8. Plan limits are enforced
9. AI Assistant provides context-aware responses
10. Real-time updates recalculate metrics

---

## Next Steps After Testing

1. **Production Deployment**: Deploy to cloud provider
2. **Monitoring Setup**: Add Sentry, DataDog, or similar
3. **Backup Strategy**: Implement database backups
4. **Load Balancing**: Add if expecting high traffic
5. **CDN Setup**: For static assets
6. **SSL Certificates**: Enable HTTPS
7. **Environment Variables**: Move secrets to vault
8. **CI/CD Pipeline**: Automate testing and deployment

**Happy Testing! 🚀**
