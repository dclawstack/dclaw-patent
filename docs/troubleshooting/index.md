# Troubleshooting

Common issues and solutions for DClaw Patent.

## Quick Diagnostics

```bash
# Check app pods
kubectl get pods -n dclaw-patent

# Check logs
kubectl logs -n dclaw-patent deployment/dclaw-patent-backend

# Check database
kubectl get clusters -n dclaw-patent
```

## Sections

- [Common Issues](./common-issues)
- [FAQ](./faq)
