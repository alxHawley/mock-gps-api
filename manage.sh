#!/bin/bash

# Mock GPS API Management Script

case "$1" in
    start)
        echo "Starting Mock GPS API..."
        docker-compose up -d
        echo "Service started. Check logs with: docker-compose logs -f"
        ;;
    stop)
        echo "Stopping Mock GPS API..."
        docker-compose down
        echo "Service stopped."
        ;;
    restart)
        echo "Restarting Mock GPS API..."
        docker-compose down
        docker-compose up -d
        echo "Service restarted."
        ;;
    logs)
        echo "Showing logs..."
        docker-compose logs -f
        ;;
    status)
        echo "Service status:"
        docker-compose ps
        ;;
    build)
        echo "Building Docker image..."
        docker-compose build
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|logs|status|build}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the service"
        echo "  stop    - Stop the service"
        echo "  restart - Restart the service"
        echo "  logs    - Show service logs"
        echo "  status  - Show service status"
        echo "  build   - Build Docker image"
        exit 1
        ;;
esac 