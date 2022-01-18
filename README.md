# fastapi_course

- To run the entire process of container creation, run in terminal
  <docker-compose up -d>
  You can also add at the end <--build> if you want to the image to be rebuild from scratch.
  It might be needed if you have already run this command before and want to make new container from scratch

- To stop all the containers that are part of the same app ran from <docker-compose>, you can run
  <docker-compose down -v>

- After running "docker-compose" and making sure both containers run ok, run command
  <docker-compose exec api alembic upgrade head> to migrage/create DB tables with alembic
  <docker-compose exec> - is a docker command to execute code in a container lauched with docker-compose
  <api> - is the name of container in which the command needs to run
