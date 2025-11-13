using System;
using CoastyApi.Models;

namespace CoastyApi.Contracts
{
    public interface ICoastyContract
    {
        Task<string> GetNameTest(User user);
        Task<object> GetAvgWaterLevels(WaterLvlRequest request);
        Task<object> GetRisks(string city, string year);
        Task<NewsReportResult> GetNews(NewsRequest request);
    }
}