## Deployment

1. **Delete the existing virtual environment**

   * Ensures no leftover or copied dependencies

2. **Create and activate a fresh environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Run the project**

   ```bash
   uvicorn main:app
   ```

   (or your actual entry point)

4. **When an error appears**

   ```text
   ModuleNotFoundError: No module named 'xyz'
   ```

   Install it:

   ```bash
   pip install xyz
   ```

5. **Repeat**

   * Run project again
   * Install next missing dependency
   * Continue until the app runs correctly

6. **Lock everything**

   ```bash
   pip freeze > requirements.txt
   ```

---

## Pending Changes

1. fix bulk delete route
2. make pagination feature


# Backend for Al-Qasira 

to use: clone repo and run following in terminal

```
venv\Scripts\activate
```
---
```
pip install -r requirements.txt
```
---
```
uvicorn app.main:app --reload
```

