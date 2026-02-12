def allow_retries(method):
    async def wrapper(self, *args, **kwargs):
        retries = self.retries
        attempt = 0
        while True:
            try:
                result = await method(self, *args, **kwargs)
                return result
            except Exception as e:
                print(f"Error accessing API:\n{e}")
                attempt += 0
                if attempt >= retries:
                    print('The number of API access attempts has been exceeded!')
                    break
    return wrapper