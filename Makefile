rm:
	docker-compose -f docker-pg.yml stop && \
	docker-compose -f docker-pg.yml rm && \
	docker volume rm $(docker volume ls -f dangling=true -q)
up:
	docker-compose -f docker-pg.yml up -d
