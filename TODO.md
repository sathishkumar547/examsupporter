# TODO: Modify Flask Student Exam Supporter for Material Filtering

## Task Summary
Modify the project to correctly filter materials when selecting University and Subject.

## Plan

### 1. Database Changes
- [ ] Add "subject" column to materials table in schema.sql

### 2. Backend Changes (app.py)
- [ ] Update upload route to save subject field
- [ ] Modify materials route to search by subject (not title)
- [ ] Add new /search route as per requirement

### 3. Frontend Changes
- [ ] Update dashboard.html search form action (if needed)
- [ ] Create search.html template with proper display
- [ ] Update materials.html to display subject field

### 4. Testing
- [ ] Test upload with subject
- [ ] Test search by university and subject
- [ ] Verify search results display correctly
