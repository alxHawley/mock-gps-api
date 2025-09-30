# Kubernetes Multi-Instance Design

## Current Architecture Analysis

### Application Characteristics
- **Stateless**: No database dependencies
- **In-memory state**: `dog_index`, `user_index`, `show_dog` are per-instance
- **File dependency**: Reads `route.gpx` file
- **Threading**: Uses background threads for simulation
- **Authentication**: API key-based (per-instance)

### Current State Management
```python
# Per-instance state (lines 21-27 in app.py)
route_points = []  # Loaded from GPX file
dog_index = 0      # Per-instance counter
user_index = 0     # Per-instance counter  
show_dog = False   # Per-instance flag
```

## Kubernetes Architecture Design

### 1. Multi-Instance Behavior
**✅ PERFECT for Kubernetes!** Each pod will have:
- **Independent state**: Each pod maintains its own `dog_index`, `user_index`, `show_dog`
- **Same GPX route**: All pods read the same `route.gpx` file
- **Independent simulation**: Each pod runs its own background threads
- **Load balancing**: Different clients can hit different pods

### 2. Scaling Strategy

#### Horizontal Pod Autoscaling (HPA)
```yaml
# Target: CPU utilization 70%
# Min pods: 2
# Max pods: 10
# Scale up: 2 pods per 15 seconds
# Scale down: 1 pod per 60 seconds
```

#### Vertical Pod Autoscaling (VPA)
```yaml
# Auto-adjust CPU/memory requests
# Mode: "Auto" (can restart pods)
# Update policy: "Off" (manual approval)
```

### 3. Resource Requirements

#### CPU/Memory Analysis
- **Current**: Single container, ~50MB RAM, minimal CPU
- **Per pod**: 100m CPU, 128Mi memory (requests)
- **Per pod**: 500m CPU, 256Mi memory (limits)
- **GPX file**: ~450KB (route.gpx)

#### Storage Requirements
- **ConfigMap**: For `route.gpx` file
- **Secrets**: For API keys
- **No persistent storage needed**

### 4. Networking Design

#### Service Types
1. **ClusterIP**: Internal communication
2. **LoadBalancer**: External access (if cloud)
3. **Ingress**: HTTP routing with SSL termination

#### Load Balancing Strategy
- **Round-robin**: Default Kubernetes behavior
- **Session affinity**: Not needed (stateless)
- **Health checks**: Built-in readiness/liveness probes

### 5. Configuration Management

#### ConfigMaps
```yaml
# route.gpx file
apiVersion: v1
kind: ConfigMap
metadata:
  name: gpx-route
data:
  route.gpx: |
    # GPX file content
```

#### Secrets
```yaml
# API keys and sensitive config
apiVersion: v1
kind: Secret
metadata:
  name: gps-api-secrets
type: Opaque
data:
  GPS_API_KEY: <base64-encoded-key>
  ALLOWED_HOSTS: <base64-encoded-hosts>
```

### 6. Deployment Strategy

#### Rolling Updates
- **Strategy**: RollingUpdate
- **Max unavailable**: 1 pod
- **Max surge**: 2 pods
- **Zero-downtime**: Maintains service availability

#### Health Checks
```yaml
# Liveness probe
livenessProbe:
  httpGet:
    path: /user_location
    port: 5001
    httpHeaders:
    - name: X-API-Key
      value: <api-key>
  initialDelaySeconds: 30
  periodSeconds: 30

# Readiness probe  
readinessProbe:
  httpGet:
    path: /user_location
    port: 5001
    httpHeaders:
    - name: X-API-Key
      value: <api-key>
  initialDelaySeconds: 10
  periodSeconds: 10
```

## Multi-Instance Considerations

### 1. State Independence
**✅ Each pod is completely independent:**
- Different clients can hit different pods
- Each pod maintains its own simulation state
- No shared state between pods
- Perfect for load balancing

### 2. Client Behavior
**Scenario**: Client A hits Pod 1, Client B hits Pod 2
- **Client A**: Gets Pod 1's user/dog positions
- **Client B**: Gets Pod 2's user/dog positions  
- **Different simulations**: Each pod runs independently
- **No conflicts**: Pods don't interfere with each other

### 3. Scaling Triggers
- **CPU utilization**: Primary scaling metric
- **Memory usage**: Secondary metric
- **Custom metrics**: Request rate, response time
- **Time-based**: Scale up during peak hours

## Questions & Considerations

### 1. State Synchronization
**Q**: Do you want all pods to show the same user/dog positions?
**A**: Current design = NO (each pod independent)
**Alternative**: Shared state via Redis/database

### 2. Client Session Affinity
**Q**: Should clients stick to the same pod?
**A**: Current design = NO (stateless)
**Alternative**: Session affinity for consistent state

### 3. Scaling Behavior
**Q**: How should pods behave when scaling?
**A**: New pods start fresh simulation
**Alternative**: State transfer between pods

### 4. Monitoring & Observability
**Q**: How to monitor multiple instances?
**A**: Prometheus + Grafana + centralized logging
**Metrics**: Per-pod and aggregate metrics

### 5. Resource Limits
**Q**: What are the resource constraints?
**A**: Depends on cluster size and requirements
**Recommendation**: Start conservative, scale up

## Implementation Plan

### Phase 1: Basic K8s Deployment
1. Create basic Deployment manifest
2. Add ConfigMap for GPX file
3. Add Secret for API keys
4. Test single pod deployment

### Phase 2: Multi-Instance Setup
1. Scale to 2-3 pods
2. Add LoadBalancer service
3. Test load balancing
4. Verify independent state

### Phase 3: Auto-scaling
1. Add HPA configuration
2. Add VPA configuration
3. Test scaling behavior
4. Monitor performance

### Phase 4: Production Ready
1. Add Ingress controller
2. Add monitoring stack
3. Add logging aggregation
4. Add backup/restore

## Questions for You

1. **State consistency**: Do you want all pods to show the same simulation, or is independent state OK?

2. **Client behavior**: Should clients be able to switch between pods, or stick to one?

3. **Scaling triggers**: What metrics should trigger scaling? (CPU, memory, request rate?)

4. **Resource limits**: What are your cluster constraints? (CPU, memory, node count?)

5. **Monitoring**: Do you want centralized monitoring, or per-pod monitoring?

6. **Deployment strategy**: Rolling updates OK, or need blue-green deployment?

7. **External access**: How should external clients access the API? (LoadBalancer, Ingress, NodePort?)

8. **Configuration**: Should API keys be the same across all pods, or different per pod?

Let me know your thoughts on these questions, and I'll create the specific Kubernetes manifests!
