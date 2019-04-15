# postgres
## start process
`docker run -d -e POSTGRES_PASSWORD=dend -e POSTGRES_USER=postgres --name postgres -p 5432:5432 -v `PWD`/postgres_db:/var/lib/postgresql/data -d postgres`


