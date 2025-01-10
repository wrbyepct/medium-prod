## 9.1.0 (2025-01-10)

### Feat

- add Elasticsearch full-text search on Article List view.

### Fix

- set Article db-level '-created_at' ordering by default; allow ArticleListView sorting on 'created_at' and 'title'

## 9.0.1 (2025-01-05)

### Fix

- All urls that take id as part of url now take uuid
- Allow user select existing category while adding a bookmark
- Allow directly create Bookmark category without adding bookmark. Fix bookmark slug auto generate missing hash part.
- Swap pkid and id on TimstampModel. Fix user doesn't have default 'Reading list' on create
- Refactor Follower/Following list view and optimize the list query..
- Fix fail to validate user email and remove redundant instance saving code.

## 9.0.0 (2025-01-01)

### Feat

- **Bookmark-category**: Refine Bookmark features
- Add bookmarks_count field in ReadingCategory
- Implement ReadingCategory model and its through table with bookmark.

### Fix

- Remove replies_count from Response model
- Remove redundant code in BookmarkDestroyView
- Optimize Bookmark all operations query
- Remove 'responses_count' from Article model
- ReadingCategory's boomkmark count is normalized, removed from model fields.
- ReadingCategory's boomkmark count is now updated through signals. Bookmarkcategory Update & Destory view finished.
- ReadingCategory is now sorted by -is_reading_list, -bookmark_count in db
- Re-implement bookmark create: user can now create bookmark with specified category

## 8.1.1 (2024-12-28)

### Refactor

- **response-signal**: Optimize response count, response clap count update signal

## 8.1.0 (2024-12-28)

### Feat

- **response**: Fix error in response count update through signal. Add ResponseManager to extract long optimized query. Remove redudant instance check in view
- Implement Response update destory feature.
- **response-view**: Implement Response List & Create view, use index to optimize list query
- add Response serializer, signals.
- add Response admin
- **response-model**: Add a article response model using mptt and TimestampModel as the base model

## 8.0.0 (2024-12-23)

### Feat

- **clap**: add clap feature, user can now clap and unclap an article

## 7.0.0 (2024-12-21)

### Feat

- **bookmark**: Add bookmark features allowing user to add, delete, and see their bookmarks

## 6.0.0 (2024-12-10)

### Feat

- **rating**: Add rating CRUD features

## 5.0.0 (2024-12-08)

### Feat

- **aritcle-features**: Add article CRUD features

## 4.0.0 (2024-11-30)

### Feat

- **profile**: Add profile view funcitonalities: list profiles, get detailed profile, partial-update profile, follow/unfollow, show my followers and get list of followings

## 3.0.0 (2024-11-20)

### Feat

- **Authentication**: Add simple jwt authentication routes

## 2.4.0 (2024-09-20)

### Feat

- **celery**: set up celery, redis, flower containers

## 2.3.0 (2024-09-17)

### Feat

- **nginx**: setup nginx docker service

## 2.2.0 (2024-09-16)

### Feat

- **user**: Add user model, user model structural test, admin, and api doc

## 2.1.0 (2024-09-11)

### Feat

- **postgres**: add backup, restore script for database

## 2.0.0 (2024-09-08)

### Feat

- **./docker/local/postgres**: add scripts for db backups & edit Dockerfile

## 1.0.0 (2024-09-07)

### Feat

- **./docker/local/postgres**: add scripts for db backups & edit Dockerfile
