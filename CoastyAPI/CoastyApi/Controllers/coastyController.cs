using Microsoft.AspNetCore.Mvc;
using YamlDotNet.Core.Tokens;
using Microsoft.AspNetCore.Authorization;
using CoastyApi.Models;
using CoastyApi.Contracts;

namespace coastAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class CoastyController : ControllerBase
{
    private readonly ILogger<CoastyController> _logger;
    private readonly ICoastyContract _coastyContract;

    public CoastyController(ILogger<CoastyController> logger, ICoastyContract coastyContract)
    {
        _logger = logger;
        _coastyContract = coastyContract;
    }

    [HttpGet("setup/Test")]
    public IActionResult Test()
    {
        return Ok();
    }

    [HttpPost("setup/GetUserTest")]
    public async Task<IActionResult> TestUser (User user)
    {
        try
        {
            var userName = await _coastyContract.GetNameTest(user);
            return Ok(new {UserName = userName});
        }
        catch (Exception ex)
        {
           Console.WriteLine($"Failure To Get User Name: {ex}");
           return StatusCode(500,"Error Getting User Name");
        }
    }
}