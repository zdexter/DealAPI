DealAPI
=======

Deployment:

1) Enter the virtual environment:
  cd [directory with repository clone] && source venv/bin/activate

2) Use Fabric to deploy

To set up DealAPI on a host called "demo" configured in your ~/.ssh/config:
  fab -R prod setup_server

To deploy to "demo":
  fab -R prod deploy