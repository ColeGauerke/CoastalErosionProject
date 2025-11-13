using Newtonsoft.Json;

namespace CoastyApi.Models
{
    public class User
    {
        public string? name { get; set; }
    }

    public class WaterLvlRequest
    {
        public string? startDate { get; set; }
        public string? endDate { get; set; }
        public string city { get; set; }
        public string state { get; set; }
        public string period { get; set; }
    }

    public class RiskRequest
    {
        public string city { get; set; }
        public int year { get; set; }
    }

    public class NewsRequest
    {
        public bool everything { get; set; }
        public string keyword { get; set; }
        public string area { get; set; }
        public DateTime searchDate { get; set; }
    }

    public class NewsArticle
    {
        public string? name { get; set; }
        public string? author { get; set; }
        public string? title { get; set; }
        public string? description { get; set; }
        public string url { get; set; }
        public DateTime? publishDate { get; set; }
    }

    public class NewsReportResult
    {
        public int totalResults { get; set; }
        public List<NewsArticle> articles { get; set; }
    }
}