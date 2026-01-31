-- ============================================================================
-- Ion Landscape Tilemaker Configuration
-- Serbian Worldview: Kosovo as Autonomous Province (admin-4), not country
-- ============================================================================
--
-- This process.lua implements the "RS" (Serbia) worldview by downgrading
-- Kosovo from admin_level=2 (country) to admin_level=4 (region).
-- 
-- The result: No international border is drawn between Serbia and Kosovo.
-- Kosovo appears as an internal administrative region, not a separate country.
--
-- Based on OpenMapTiles schema with modifications for Serbian cartographic view.
-- ============================================================================

-- Lua helper functions
function Set(list)
    local set = {}
    for _, l in ipairs(list) do set[l] = true end
    return set
end

-- Define which OSM tags we want to read
node_keys = { "place", "name", "population", "capital", "admin_level" }

-- ============================================================================
-- KOSOVO DETECTION HELPER
-- Returns true if this boundary relation represents Kosovo as admin-0
-- ============================================================================
function is_kosovo_admin0(tags)
    -- Must be admin_level 2 (country-level)
    if tags.admin_level ~= "2" then 
        return false 
    end
    
    -- Check by name
    if tags.name then
        local name = string.lower(tags.name)
        if name == "kosovo" or name == "kosova" or name == "република косово" or 
           name == "republika e kosovës" or name == "republic of kosovo" then
            return true
        end
    end
    
    -- Check by ISO code (Kosovo uses XK unofficially)
    if tags["ISO3166-1"] == "XK" or tags["ISO3166-1:alpha2"] == "XK" or
       tags["iso_a2"] == "XK" or tags["ISO3166-2"] and string.find(tags["ISO3166-2"], "^XK") then
        return true
    end
    
    -- Check Wikidata ID for Kosovo (Q1246)
    if tags.wikidata == "Q1246" then
        return true
    end
    
    return false
end

-- ============================================================================
-- NODE PROCESSING
-- Handles places (cities, towns, countries, etc.)
-- ============================================================================
function node_function()
    local place = Find("place")
    if place == "" then return end
    
    local name = Find("name")
    if name == "" then return end
    
    local mz = 99
    local kind = ""
    
    if place == "country" then
        -- Kosovo should not appear as a country label
        if string.lower(name) == "kosovo" or string.lower(name) == "kosova" then
            -- Downgrade to region label
            kind = "region"
            mz = 6
        else
            kind = "country"
            mz = 0
        end
    elseif place == "state" or place == "region" then
        kind = "region"
        mz = 4
    elseif place == "city" then
        kind = "city"
        mz = 4
        local pop = tonumber(Find("population")) or 0
        if pop > 1000000 then mz = 2
        elseif pop > 500000 then mz = 3
        elseif pop > 100000 then mz = 4
        end
    elseif place == "town" then
        kind = "town"
        mz = 7
    elseif place == "village" then
        kind = "village"
        mz = 10
    elseif place == "hamlet" then
        kind = "hamlet"
        mz = 12
    else
        return
    end
    
    Layer("place", false)
    Attribute("class", kind)
    Attribute("name", name)
    MinZoom(mz)
    
    local name_en = Find("name:en")
    if name_en ~= "" then Attribute("name_en", name_en) end
    
    local pop = Find("population")
    if pop ~= "" then AttributeNumeric("population", tonumber(pop) or 0) end
end

-- ============================================================================
-- WAY PROCESSING  
-- Handles roads, water, landuse, buildings
-- ============================================================================
function way_function()
    local dominated = false
    
    -- Highway/road processing
    local highway = Find("highway")
    if highway ~= "" then
        local dominated = false
        Layer("transportation", false)
        
        local class = ""
        local mz = 14
        
        if highway == "motorway" or highway == "motorway_link" then
            class = "motorway"
            mz = 4
        elseif highway == "trunk" or highway == "trunk_link" then
            class = "trunk"
            mz = 5
        elseif highway == "primary" or highway == "primary_link" then
            class = "primary"
            mz = 6
        elseif highway == "secondary" or highway == "secondary_link" then
            class = "secondary"
            mz = 8
        elseif highway == "tertiary" or highway == "tertiary_link" then
            class = "tertiary"
            mz = 10
        elseif highway == "residential" or highway == "unclassified" then
            class = "minor"
            mz = 12
        elseif highway == "service" then
            class = "service"
            mz = 14
        elseif highway == "path" or highway == "footway" or highway == "cycleway" then
            class = "path"
            mz = 14
        else
            return
        end
        
        Attribute("class", class)
        MinZoom(mz)
        return
    end
    
    -- Water (areas)
    local waterway = Find("waterway")
    local natural = Find("natural")
    local landuse = Find("landuse")
    
    if natural == "water" or landuse == "reservoir" or landuse == "basin" then
        Layer("water", true)
        MinZoom(4)
        return
    end
    
    if waterway == "riverbank" then
        Layer("water", true)
        MinZoom(6)
        return
    end
    
    if waterway == "river" or waterway == "canal" then
        Layer("waterway", false)
        Attribute("class", waterway)
        MinZoom(8)
        return
    end
    
    -- Landcover
    if natural == "wood" or natural == "forest" or landuse == "forest" then
        Layer("landcover", true)
        Attribute("class", "wood")
        MinZoom(7)
        return
    end
    
    if natural == "grassland" or landuse == "grass" or landuse == "meadow" then
        Layer("landcover", true)
        Attribute("class", "grass")
        MinZoom(9)
        return
    end
    
    -- Landuse
    if landuse == "residential" then
        Layer("landuse", true)
        Attribute("class", "residential")
        MinZoom(10)
        return
    end
    
    if landuse == "industrial" or landuse == "commercial" then
        Layer("landuse", true)
        Attribute("class", landuse)
        MinZoom(10)
        return
    end
    
    -- Parks
    if landuse == "park" or Find("leisure") == "park" then
        Layer("park", true)
        MinZoom(10)
        return
    end
    
    -- Buildings
    local building = Find("building")
    if building ~= "" and building ~= "no" then
        Layer("building", true)
        MinZoom(13)
        return
    end
end

-- ============================================================================
-- RELATION PROCESSING
-- Handles administrative boundaries - THIS IS WHERE KOSOVO IS FIXED
-- ============================================================================
function relation_scan_function()
    if Find("type") == "boundary" and Find("boundary") == "administrative" then
        Accept()
    end
    if Find("type") == "multipolygon" then
        Accept()
    end
end

function relation_function()
    local reltype = Find("type")
    
    if reltype == "boundary" then
        local boundary = Find("boundary")
        local admin_level = Find("admin_level")
        
        if boundary == "administrative" and admin_level ~= "" then
            local level = tonumber(admin_level)
            if level == nil then return end
            
            -- ================================================================
            -- 🔴 KOSOVO HANDLING - SERBIAN WORLDVIEW (RS)
            -- Downgrade Kosovo from admin-0 (country) to admin-4 (region)
            -- ================================================================
            local is_kosovo = false
            local name = string.lower(Find("name"))
            
            -- Check by name
            if name == "kosovo" or name == "kosova" or name == "република косово" or 
               name == "republika e kosovës" or name == "republic of kosovo" then
                is_kosovo = true
            end
            
            -- Check by ISO code
            if not is_kosovo then
                local iso = Find("ISO3166-1")
                local iso2 = Find("ISO3166-1:alpha2")
                local isoching = Find("iso_a2")
                if iso == "XK" or iso2 == "XK" or isoching == "XK" then
                    is_kosovo = true
                end
            end
            
            -- Check Wikidata
            if not is_kosovo and Find("wikidata") == "Q1246" then
                is_kosovo = true
            end

            if is_kosovo and (admin_level == "2" or level == 2) then
                -- Option A: Downgrade to regional boundary (admin_level 4)
                level = 4
                admin_level = "4"
                
                -- Log this for debugging
                print("Kosovo boundary detected - downgrading from admin-0 to admin-4 (Serbian worldview)")
            end
            
            -- Only process admin levels 2-6
            if level < 2 or level > 6 then return end
            
            Layer("boundary", false)
            Attribute("admin_level", level)
            
            -- Set min zoom based on admin level
            local mz = 0
            if level == 2 then mz = 0
            elseif level == 3 then mz = 3
            elseif level == 4 then mz = 5
            elseif level == 5 then mz = 8
            elseif level == 6 then mz = 10
            end
            MinZoom(mz)
            
            -- Add name if present
            local name = Find("name")
            if name ~= "" then
                Attribute("name", name)
            end
        end
    end
    
    if reltype == "multipolygon" then
        way_function()
    end
end

-- ============================================================================
-- Attribution (required for ODbL compliance)
-- ============================================================================
attribute_function = function(v,layer)
    return {}
end

-- Print startup message
print("===========================================")
print("Ion Landscape Tile Generator")
print("Worldview: RS (Serbia)")
print("Kosovo: Treated as admin-4 (region), not admin-0 (country)")
print("===========================================")
