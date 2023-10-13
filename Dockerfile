ARG BASE_IMAGE=ghcr.io/nationalarchives/tna-python-django
ARG BASE_IMAGE_TAG=latest
FROM "$BASE_IMAGE":"$BASE_IMAGE_TAG"

ENV NPM_BUILD_COMMAND=compile
ENV DJANGO_SETTINGS_MODULE=config.settings.production

# Copy in the project dependency files and config
COPY --chown=app pyproject.toml poetry.lock ./
COPY --chown=app package.json package-lock.json .nvmrc webpack.config.js ./
COPY --chown=app sass sass
COPY --chown=app scripts scripts
COPY --chown=app config config
COPY --chown=app templates templates

# Install Python dependencies AND the 'etna' app
RUN tna-build

# Copy application code
COPY --chown=app . .

# Copy the assets from the @nationalarchives/frontend repository
RUN mkdir -p /app/templates/static/assets; \
  cp -R /app/node_modules/@nationalarchives/frontend/nationalarchives/assets/* /app/templates/static/assets

CMD ["tna-run", "config.wsgi:application"]
