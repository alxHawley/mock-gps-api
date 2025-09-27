#!/bin/bash

# Mock GPS API Management Script

case "$1" in
    start)
        echo "Starting Mock GPS API..."
        docker-compose up -d
        ;;
    stop)
        echo "Stopping Mock GPS API..."
        docker-compose down
        ;;
    restart)
        echo "Restarting Mock GPS API..."
        docker-compose restart
        ;;
    logs)
        echo "Showing Mock GPS API logs..."
        docker-compose logs -f
        ;;
    status)
        echo "Mock GPS API status:"
        docker-compose ps
        ;;
    build)
        echo "Building Mock GPS API..."
        docker-compose build
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|logs|status|build}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the API service"
        echo "  stop    - Stop the API service"
        echo "  restart - Restart the API service"
        echo "  logs    - Show API logs"
        echo "  status  - Show API status"
        echo "  build   - Build the API container"
        exit 1
        ;;
esac
