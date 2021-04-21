some tests for alaska bears:

Functional:

1. Single bear creation (all valid bear types + valid names (ru/en/etc) + valid age (different formats)).
Created bear should be returned by id and by get all request

2. Single bear creation negative cases (invalid bear types/invalid names/invalid age in different
combinations + invalid json). Status code should be like 400. Created bear should NOT be returned by id and by
get all request

3. Multiple bear creation
3.1. Sequential
3.1.1. Bears with same input parameters. Resulted ids should be different
3.1.2. Create bears one by one. Bears should be returned by id and by get all request
3.2. Parallel (issue a bunch of parallel creation requests - results should be consistent)

4. Bear deletion. Delete by id. Delete by invalid id. Delete all.

5. Bear update.
5.1 Update all existing parameters (type, name, age, id) with valid values
5.2 Update all existing parameters (type, name, age, id) with invalid values
5.3 Update removed bear
5.4 Parallel updates of one bear. Results should be consistent

6. Fuzzy cases - create/update/get/delete in different random combinations. Run for 10 minutes for instance. Results
should be consistent.

Load:

1. Lets say we should process 100 requests per second. Generate such load. Check our service is responsive and results
are consistent

Stress:

1. Create as much bears as possible while service is responsive. Generate stress load with a huge amount of
invalid/valid requests from single IP. From multiple IPs.

Security:

1. Use sql/js/etc inside input parameters (or just instead of json) for create/update requests.
2. Use sql/js/etc inside url (as an id param for instance) for create/update/delete requests.

Rest compliance:

1. Verify that every response from service contain valid response code due to rest specification

