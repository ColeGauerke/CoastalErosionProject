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
    public class EventReportRequest
    {
        public string EventType { get; set; } = string.Empty;
        public string Severity { get; set; } = string.Empty;
        public DateTime ObservedAt { get; set; }
        public string LocationText { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;

        public string? ContactName { get; set; }
        public string? ContactEmail { get; set; }
    }
    public class EventReport
    {
        public int Id { get; set; }

        public string EventType { get; set; } = string.Empty;
        public string Severity { get; set; } = string.Empty;
        public DateTime ObservedAt { get; set; }
        public string LocationText { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;

        public string? ContactName { get; set; }
        public string? ContactEmail { get; set; }

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
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