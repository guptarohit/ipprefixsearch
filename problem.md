# IP Prefix Lookup Optimal Solution

Assume there's a script that collects a list of IP subnets owned by all the public service providers. These IP subnets with their prefixes are provided in `prefixes.json` file. Each subnet has a Cloud Service Provider and some tag(s) attached to them. Each IP Subnet will consist of multiple IP addresses, based on the prefix. The biggest subnet we can have is /8 (16,777,216 IPs) and smallest subnet is /32 (1 IP).

As a user, we are going to provide either a single IP address or list of IP addresses via REST API. These IP(s) might or might not belong to the above IP subnets. Also these (IPs) could belong to multiple subnets. The expected output is name of the Cloud Service Provider and related tag(s), if matched for user input.

Example: The provided data contains “184.51.33.0/24” with “Akamai” as provider and “Cloud”, “CDN/WAF” as tags. So if user provides “184.51.33.230” as an input, the API should return something like `{“result”: [{“subnet”: “184.51.33.0/24”, “provider”: “Akamai”, “tags”: [“Cloud”, “CDN/WAF”]}]}` as output. As mentioned above, there could be multiple matching subnets.

Your task is to find a solution that's:
* The most efficient way to store this data. 
* The fast way to figure out if a user provided IP address belongs to a certain Cloud Provider Prefix or not?
* The ideal time for looking this up should be less than ~300ms for a batch of 10 IP addreses.
* Searching a single IP address should be less than ~50ms. (excluding N/W trip time)
* A single IP could belong to multiple subnets too.
* You can prepare/model the data as per your preference, if needed.
* Feel free to use any database for the task. Using a database is not mandatory.


Build RESTful endpoint(s) to search in Python (FastAPI):
 * Single IP address
 * Multiple IP addresses (batch)

Follow the RESTful design standards and coding standards. The code should be up to prod standards and follow best practices.

## References

You can read more about IP Prefixes and Subnets here:
* https://www.cloudflare.com/learning/network-layer/what-is-a-subnet/
* https://medium.com/netdevops/what-are-network-prefixes-e1923a1d6a3e
* https://avinetworks.com/glossary/subnet-mask/
* https://www.calculator.net/ip-subnet-calculator.html

