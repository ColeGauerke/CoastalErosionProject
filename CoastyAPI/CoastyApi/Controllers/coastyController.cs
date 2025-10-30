using Microsoft.AspNetCore.Mvc;
using YamlDotNet.Core.Tokens;
using Microsoft.AspNetCore.Authorization;
using CoastyApi.Models;
using CoastyApi.Contracts;
using Microsoft.EntityFrameworkCore;
using CoastalErosion.Data;

namespace coastAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class CoastyController : ControllerBase
{
    private readonly ILogger<CoastyController> _logger;
    private readonly ICoastyContract _coastyContract;
    private readonly CoastalErosionDbContext _db;

    public CoastyController(ILogger<CoastyController> logger, ICoastyContract coastyContract, CoastalErosionDbContext db)
    {
        _logger = logger;
        _coastyContract = coastyContract;
        _db = db;
    }

    [HttpGet("setup/Test")]
    public IActionResult Test()
    {
        return Ok();
    }

    [HttpGet("setup/TestDbConnection")]
    public async Task<IActionResult> TestConnect()
    {
        try
        {
            var canConnect = await _db.Database.CanConnectAsync();
            if (canConnect)
            {
                return Ok(new { 
                    message = "Database connection successful!",
                    connected = true 
                });
            }
            else
            {
                return StatusCode(500, new { 
                    message = "Cannot connect to database",
                    connected = false 
                });
            }
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Invalid DB Connection: {ex.Message}");
        }
    }

    [HttpPost("setup/GetUserTest")]
    public async Task<IActionResult> TestUser(User user)
    {
        try
        {
            var userName = await _coastyContract.GetNameTest(user);
            return Ok(new { UserName = userName });
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Failure To Get User Name: {ex}");
            return StatusCode(500, "Error Getting User Name");
        }
    }
    
    [HttpPost("GetVerifiedWaterLevels")]
    public async Task<IActionResult> GetVerifiedWaterLvls (WaterLvlRequest user)
    {
        try
        {
            var userName = await _coastyContract.GetAvgWaterLevels(user);
            return Ok(userName);
        }
        catch (Exception ex)
        {
           Console.WriteLine($"Failure To Get Verified Water Levls: {ex}");
           return StatusCode(500,"Error Getting Verified Water Levls");
        }
    }
}