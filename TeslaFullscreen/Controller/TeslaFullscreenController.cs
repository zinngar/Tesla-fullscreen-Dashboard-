using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using TeslaFullscreen.Configuration;

namespace TeslaFullscreen.Controller;

/// <summary>
/// API Controller for managing and accessing Tesla Fullscreen links.
/// </summary>
[ApiController]
[Route("TeslaFullscreen")]
[Authorize]
[ApiExplorerSettings(IgnoreApi = true)]
public class TeslaFullscreenController : ControllerBase
{
    /// <summary>
    /// Gets the list of saved Tesla Links.
    /// </summary>
    /// <returns>A list of saved Tesla Links.</returns>
    [HttpGet("Links")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    public ActionResult<IEnumerable<TeslaLink>> GetLinks()
    {
        var config = Plugin.Instance?.Configuration;
        if (config == null)
        {
            return NotFound("Plugin configuration not found.");
        }

        return Ok(config.Links ?? Array.Empty<TeslaLink>());
    }

    /// <summary>
    /// Adds a new Tesla Link. Only accessible by administrators.
    /// </summary>
    /// <param name="newLink">The new link to add.</param>
    /// <returns>A status action result.</returns>
    [HttpPost("Links")]
    [Authorize(Policy = "RequiresAdmin")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public ActionResult AddLink([FromBody] TeslaLink newLink)
    {
        if (newLink == null || string.IsNullOrWhiteSpace(newLink.Name) || string.IsNullOrWhiteSpace(newLink.Url))
        {
            return BadRequest("Name and URL are required.");
        }

        var plugin = Plugin.Instance;
        if (plugin == null)
        {
            return NotFound("Plugin instance not found.");
        }

        var config = plugin.Configuration;
        var list = config.Links?.ToList() ?? new List<TeslaLink>();

        if (list.Any(l => string.Equals(l.Name, newLink.Name, StringComparison.OrdinalIgnoreCase)))
        {
            return BadRequest("A link with this name already exists.");
        }

        list.Add(newLink);
        config.Links = list.ToArray();

        plugin.SaveConfiguration(config);
        return Ok();
    }

    /// <summary>
    /// Deletes a Tesla Link. Only accessible by administrators.
    /// </summary>
    /// <param name="name">The name of the link to delete.</param>
    /// <returns>A status action result.</returns>
    [HttpDelete("Links")]
    [Authorize(Policy = "RequiresAdmin")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public ActionResult DeleteLink([FromQuery] string name)
    {
        if (string.IsNullOrWhiteSpace(name))
        {
            return BadRequest("Link name is required.");
        }

        var plugin = Plugin.Instance;
        if (plugin == null)
        {
            return NotFound("Plugin instance not found.");
        }

        var config = plugin.Configuration;
        var list = config.Links?.ToList() ?? new List<TeslaLink>();

        var itemToRemove = list.FirstOrDefault(l => string.Equals(l.Name, name, StringComparison.OrdinalIgnoreCase));
        if (itemToRemove == null)
        {
            return NotFound("Link not found.");
        }

        list.Remove(itemToRemove);
        config.Links = list.ToArray();

        plugin.SaveConfiguration(config);
        return Ok();
    }
}
