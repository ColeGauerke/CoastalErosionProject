using System;
using System.Threading.Tasks;
using CoastyApi.Models;
using CoastyApi.Contracts;


namespace CoastyApi.Repos
{
    public class TestRepo : ICoastyContract
    {
        public Task<string> GetNameTest (User user)
        {
            if (user.name == null)
            {
                return Task.FromResult("No Name Given");
            }
            else
            {
                return Task.FromResult(user.name);
            }
        }
    }
}