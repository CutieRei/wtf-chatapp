# If you're reading this you're fricked
but anyway

Make sure you have pdm installed (https://pdm.fming.dev/latest/#installation)

## Setup
run
```console
npm/pnpm/yarn install
```
on the root folder

and
```console
pdm install
```
inside the `server` directory (recommended to use virtualenv)

to run the server you'll need to run the python server by running `pdm run dev` in `server` (currently its in development and not suited yet for production) and `npm run dev` on the root directory
