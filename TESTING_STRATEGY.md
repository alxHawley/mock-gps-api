# API Testing Strategy & Performance Baseline

## Overview

This document outlines a comprehensive testing strategy for the Mock GPS API to establish performance baselines before implementing Kubernetes multi-instance deployment. The testing will cover unit tests, integration tests, and performance/load testing.

## Current API Analysis

### Endpoints
1. **GET /user_location** - Returns current user position (lat, lon)
2. **GET /dog_location** - Returns dog position or null if not tracking
3. **GET /user_follow_location** - Alias for user_location
4. **POST /start_tracking** - Enables dog tracking
5. **POST /stop_tracking** - Disables dog tracking
6. **GET /health** - Health check endpoint

### Authentication
- All endpoints require `X-API-Key` header
- API key validation on every request

### State Management
- Global variables: `dog_index`, `user_index`, `show_dog`
- Background threads for simulation
- GPX file loading and parsing

## Testing Architecture

### Repository-Level Tests (In-Repo)
**Purpose**: Fast feedback during development, code quality, basic functionality
**Location**: This repository (`tests/` directory)
**Trigger**: Developer commits, local testing, pre-merge checks

### External CI/CD Tests (Separate Framework)
**Purpose**: Comprehensive testing, performance validation, production readiness
**Location**: Your external test framework(s)
**Trigger**: Deployment pipeline, scheduled runs, release validation

## Testing Framework Options

### Repository-Level Testing (In-Repo)

#### 1. Python Testing Stack
**Recommended for unit tests and basic API tests**

##### Unit Testing
- **Framework**: `pytest` + `pytest-flask`
- **Coverage**: `pytest-cov`
- **Mocking**: `unittest.mock` or `pytest-mock`

##### Basic API Testing
- **HTTP Client**: `requests` + `pytest-requests`
- **Test Data**: `faker` for generating test data
- **Fixtures**: `pytest` fixtures for test setup

##### Quick Performance Tests
- **Micro-benchmarks**: `pytest-benchmark` for function-level performance
- **Basic Load**: Simple `requests`-based load testing
- **Monitoring**: `psutil` for basic system metrics

### External CI/CD Testing (Separate Framework)

#### 1. Python Testing Stack
**For comprehensive testing in your external framework**

##### Advanced API Testing
- **Framework**: `pytest` + `requests` + custom test runners
- **Test Data**: `faker` + custom data generators
- **Fixtures**: Complex test setup and teardown

##### Performance Testing
- **Load Testing**: `locust` (Python-based, easy to customize)
- **Stress Testing**: Custom Python load testing tools
- **Monitoring**: `psutil` + `prometheus` + custom metrics

#### 2. JavaScript/TypeScript Testing Stack
**For web-focused testing in your external framework**

##### API Testing
- **Framework**: `jest` + `supertest`
- **HTTP Client**: `axios` or `fetch`
- **Test Runner**: `jest` with custom test suites

##### Performance Testing
- **Load Testing**: `k6` (JavaScript-based, excellent for API testing)
- **Artillery**: Node.js-based load testing
- **Newman**: Postman collection runner

#### 3. Go Testing Stack
**For high-performance testing in your external framework**

##### Performance Testing
- **Vegeta**: HTTP load testing tool
- **Hey**: HTTP load testing tool
- **Custom Go tools**: For specific scenarios

## Testing Strategy

### Repository-Level Tests (In-Repo)
**Goal**: Fast feedback, code quality, basic functionality validation

#### Phase 1: Unit Tests (Python + pytest)
**Location**: `tests/unit/` in this repository
**Trigger**: Local development, pre-commit hooks

##### Test Coverage
- [ ] API key validation
- [ ] GPX file loading and parsing
- [ ] Route point extraction
- [ ] State management (dog_index, user_index, show_dog)
- [ ] Background thread simulation
- [ ] Error handling and edge cases

##### Test Structure
```python
# tests/unit/test_auth.py
def test_valid_api_key()
def test_invalid_api_key()
def test_missing_api_key()

# tests/unit/test_gpx.py
def test_gpx_loading()
def test_gpx_parsing()
def test_route_points_extraction()

# tests/unit/test_state.py
def test_dog_index_increment()
def test_user_index_increment()
def test_show_dog_toggle()
```

#### Phase 2: Basic API Tests (Python + requests)
**Location**: `tests/integration/` in this repository
**Trigger**: Local development, pre-merge checks

##### Test Scenarios
- [ ] Complete workflow (start tracking → get locations → stop tracking)
- [ ] Authentication flow
- [ ] Error responses (401, 500)
- [ ] Basic concurrent requests (2-5 users)
- [ ] State persistence across requests

##### Test Structure
```python
# tests/integration/test_api_endpoints.py
def test_user_location_endpoint()
def test_dog_location_endpoint()
def test_tracking_workflow()
def test_basic_concurrent_requests()
def test_error_handling()
```

#### Phase 3: Quick Performance Tests (Python + pytest-benchmark)
**Location**: `tests/performance/` in this repository
**Trigger**: Local development, pre-merge checks

##### Performance Metrics
- **Response Time**: Basic timing measurements
- **Resource Usage**: CPU, memory (basic)
- **Error Rate**: Simple error counting
- **Function Performance**: Micro-benchmarks

### External CI/CD Tests (Separate Framework)
**Goal**: Comprehensive testing, performance validation, production readiness

#### Phase 4: Advanced API Testing (Your External Framework)
**Location**: Your external test framework
**Trigger**: Deployment pipeline, scheduled runs

##### Test Scenarios
- [ ] Complete workflow validation
- [ ] Authentication flow testing
- [ ] Error response validation
- [ ] High-concurrency testing (10-50+ users)
- [ ] State persistence across requests
- [ ] Cross-browser/client testing

#### Phase 5: Performance Testing (Your External Framework)
**Location**: Your external test framework
**Trigger**: Deployment pipeline, release validation

##### Performance Metrics
- **Response Time**: P50, P95, P99 percentiles
- **Throughput**: Requests per second (RPS)
- **Resource Usage**: CPU, memory, network
- **Error Rate**: Failed requests percentage
- **Concurrent Users**: Maximum supported users

##### Load Test Scenarios
1. **Light Load**: 1-5 concurrent users
2. **Medium Load**: 10-20 concurrent users
3. **Heavy Load**: 50-100 concurrent users
4. **Stress Test**: 200+ concurrent users
5. **Sustained Load**: 30-minute continuous load

##### Test Patterns (External Framework)
```python
# External framework: locustfile.py
class APITestUser(HttpUser):
    @task(3)
    def get_user_location(self):
        self.client.get("/user_location", headers=headers)
    
    @task(2)
    def get_dog_location(self):
        self.client.get("/dog_location", headers=headers)
    
    @task(1)
    def toggle_tracking(self):
        if random.choice([True, False]):
            self.client.post("/start_tracking", headers=headers)
        else:
            self.client.post("/stop_tracking", headers=headers)
```

#### Phase 6: Advanced Performance Testing (Your External Framework)
**Location**: Your external test framework
**Trigger**: Release validation, performance regression testing

##### K6 Test Scenarios
- **Smoke Test**: Basic functionality
- **Load Test**: Expected production load
- **Stress Test**: Beyond normal capacity
- **Spike Test**: Sudden load increases
- **Volume Test**: Large amounts of data
- **Endurance Test**: Long-running tests

##### K6 Test Structure (External Framework)
```javascript
// External framework: api-load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 10 },   // Ramp up
    { duration: '5m', target: 10 },   // Stay at 10 users
    { duration: '2m', target: 50 },   // Ramp up to 50
    { duration: '5m', target: 50 },   // Stay at 50 users
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'], // 95% of requests under 200ms
    http_req_failed: ['rate<0.1'],    // Error rate under 10%
  },
};
```

## Performance Baseline Metrics

### Current Single-Container Performance
**Target Metrics to Establish:**

#### Response Time Targets
- **P50**: < 50ms
- **P95**: < 100ms
- **P99**: < 200ms
- **Max**: < 500ms

#### Throughput Targets
- **Light Load (1-5 users)**: 100+ RPS
- **Medium Load (10-20 users)**: 200+ RPS
- **Heavy Load (50+ users)**: 500+ RPS

#### Resource Usage
- **CPU**: < 70% under normal load
- **Memory**: < 128MB per instance
- **Network**: Minimal I/O

#### Error Rate
- **Target**: < 0.1% error rate
- **Acceptable**: < 1% error rate
- **Critical**: > 5% error rate

## Test Environment Setup

### 1. Test Data Preparation
- **GPX Files**: Multiple test GPX files of different sizes
- **API Keys**: Test API keys for different scenarios
- **Test Users**: Simulated user sessions

### 2. Monitoring Setup
- **System Metrics**: CPU, memory, disk I/O
- **Application Metrics**: Response times, error rates
- **Network Metrics**: Bandwidth, latency
- **Docker Metrics**: Container resource usage

### 3. Test Execution Environment
- **Isolated Environment**: Separate from production
- **Consistent Conditions**: Same hardware, network
- **Repeatable Tests**: Deterministic test execution
- **Data Collection**: Automated metrics collection

## Implementation Plan

### Repository-Level Tests (In-Repo)

#### Week 1: Unit Tests
- [ ] Set up pytest environment in repository
- [ ] Write unit tests for core functions
- [ ] Achieve 80%+ code coverage
- [ ] Add pre-commit hooks for testing

#### Week 2: Basic Integration Tests
- [ ] Set up API testing framework in repository
- [ ] Write basic integration tests
- [ ] Test complete workflows
- [ ] Validate error handling
- [ ] Add basic performance benchmarks

### External CI/CD Tests (Separate Framework)

#### Week 3: External Framework Setup
- [ ] Set up external test framework
- [ ] Create API test collections
- [ ] Set up performance testing tools (Locust/K6)
- [ ] Configure CI/CD integration

#### Week 4: Comprehensive Testing
- [ ] Create advanced test scenarios
- [ ] Establish baseline performance metrics
- [ ] Document performance characteristics
- [ ] Set up automated testing pipeline
- [ ] Prepare for Kubernetes testing

## Test Framework Selection

### Repository-Level Tests (In-Repo)
**Recommended Stack:**
1. **Unit Tests**: Python + pytest + pytest-cov
2. **Integration Tests**: Python + requests + pytest
3. **Quick Performance**: Python + pytest-benchmark
4. **Monitoring**: Python + psutil

**Rationale:**
- **Python**: Consistent with existing codebase
- **pytest**: Industry standard, excellent features
- **Lightweight**: Fast execution, minimal dependencies
- **Local Focus**: Quick feedback during development

### External CI/CD Tests (Separate Framework)
**Recommended Stack:**
1. **API Testing**: Your existing framework (Python/JS/Go)
2. **Performance Testing**: Locust (Python) or K6 (JavaScript)
3. **Load Testing**: Artillery (Node.js) or Vegeta (Go)
4. **Monitoring**: Prometheus + Grafana + custom metrics

**Rationale:**
- **Flexibility**: Use your preferred external framework
- **Power**: Advanced testing capabilities
- **Integration**: Seamless CI/CD pipeline integration
- **Scalability**: Handle complex test scenarios

## Success Criteria

### Unit Tests
- [ ] 80%+ code coverage
- [ ] All critical paths tested
- [ ] Fast execution (< 30 seconds)
- [ ] Reliable and repeatable

### Integration Tests
- [ ] All API endpoints tested
- [ ] Complete workflows validated
- [ ] Error scenarios covered
- [ ] Authentication tested

### Performance Tests
- [ ] Baseline metrics established
- [ ] Performance characteristics documented
- [ ] Bottlenecks identified
- [ ] Scaling behavior understood

## Next Steps

1. **Choose Testing Framework**: Confirm Python + pytest + Locust
2. **Set Up Test Environment**: Create isolated testing environment
3. **Write Unit Tests**: Start with core functionality
4. **Establish Baselines**: Run performance tests on current setup
5. **Document Results**: Create performance baseline report
6. **Prepare for K8s**: Use baselines to compare with Kubernetes deployment

## Summary

### Repository-Level Tests (In-Repo)
- **Purpose**: Fast feedback during development
- **Location**: `tests/` directory in this repository
- **Framework**: Python + pytest + requests
- **Scope**: Unit tests, basic integration, quick performance
- **Trigger**: Local development, pre-commit hooks

### External CI/CD Tests (Separate Framework)
- **Purpose**: Comprehensive testing, performance validation
- **Location**: Your external test framework(s)
- **Framework**: Your choice (Python/JS/Go + Locust/K6/Artillery)
- **Scope**: Advanced API testing, load testing, performance baselines
- **Trigger**: Deployment pipeline, scheduled runs

### Key Benefits
- **Separation of Concerns**: Fast local tests vs comprehensive external tests
- **Flexibility**: Use your preferred external framework
- **Efficiency**: Right tool for each job
- **Integration**: Seamless CI/CD pipeline integration

## Questions for Framework Selection

1. **External Framework**: What testing frameworks do you currently use? (Python, JavaScript, Go, etc.)

2. **Performance Tools**: Preference for Locust (Python), K6 (JavaScript), or Artillery (Node.js)?

3. **Test Scope**: Focus on API testing only, or include system-level testing?

4. **Monitoring**: Basic metrics or detailed observability stack?

5. **CI/CD Integration**: How do you currently handle testing in your deployment pipeline?

**Please review this strategy and let me know your preferences for framework selection and testing scope!**
