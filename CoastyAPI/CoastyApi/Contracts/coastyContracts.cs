using System;
using CoastyApi.Models;

namespace CoastyApi.Contracts
{
    public interface ICoastyContract
    {
        Task<string> GetNameTest (User user);
    }
}