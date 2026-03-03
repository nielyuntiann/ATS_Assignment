{
  "services": [
    {
      "name": "User API",
      "uri": "http://mock-services:4000/health",
      "expected_version": "1.2.0",
      "interval_check": 5
    },
    {
      "name": "Auth Service",
      "uri": "http://mock-services:5000/version",
      "expected_version": "3.5.1",
      "interval_check": 7
    }
  ],
  "pool": 10
}
