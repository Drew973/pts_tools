<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology" version="3.18.1-Zürich">
 <renderer-v2 forceraster="0" type="RuleRenderer" enableorderby="0" symbollevels="0">
  <rules key="{4453275f-3cf8-4976-aeb3-f400b96866d4}">
   <rule key="{9ea7a7ec-fc04-4163-a0b4-0e88c424a638}" label="CR(2)" symbol="0" filter="&quot;defectType&quot; = 'CR' and &quot;severity&quot; = '2'"/>
   <rule key="{a71175e1-6d04-4946-840b-e8e6e8aeebba}" label="CR(1)" symbol="1" filter="&quot;defectType&quot; = 'CR' and &quot;severity&quot; = '1'"/>
   <rule key="{d8ed238b-d6eb-4c5f-863e-f390174770ec}" label="CZ(2)" symbol="2" filter="&quot;defectType&quot; = 'CZ' and &quot;severity&quot; = '2'"/>
   <rule key="{93930c00-5d7e-4072-aeab-daeade2f0fcc}" label="CZ(1)" symbol="3" filter="&quot;defectType&quot; = 'CZ' and &quot;severity&quot; = '1'"/>
   <rule key="{1f96cb6c-cf52-4393-b522-05864f11d08a}" label="LP" symbol="4" filter="&quot;defectType&quot; = 'LP'"/>
   <rule key="{0b68fd4f-0790-4b61-a919-6de1ffee7805}" label="OJ(N)" symbol="5" filter="&quot;defectType&quot; = 'OJ' and &quot;severity&quot; = 'N'"/>
   <rule key="{e1416c3e-6af7-4b5b-afdb-4a26434f596e}" label="OJ(M)" symbol="6" filter="&quot;defectType&quot; = 'OJ' and &quot;severity&quot; = 'M'"/>
   <rule key="{e7e26142-a994-4456-ae8b-ea51048c8197}" label="OJ(W)" symbol="7" filter="&quot;defectType&quot; = 'OJ' and &quot;severity&quot; = 'W'"/>
   <rule key="{e667ccea-01d1-4a2f-a4ac-c33d92012c05}" label="PA(2)" symbol="8" filter="&quot;defectType&quot; = 'PA' and &quot;severity&quot; = 2"/>
   <rule key="{fe2a7300-61d1-4f14-b65e-a7eb9de8bd0c}" label="PA(1)" symbol="9" filter="&quot;defectType&quot; = 'PA' and &quot;severity&quot; = '1'"/>
   <rule key="{30ed88d4-baf6-4d51-81f9-88b6cf971716}" label="SD(2)" symbol="10" filter="&quot;defectType&quot; = 'SD' and &quot;severity&quot; = '2'"/>
   <rule key="{a622baf7-3f1b-4739-a278-4a21b2b560aa}" label="SD(1)" symbol="11" filter="&quot;defectType&quot; = 'SD' and &quot;severity&quot; = '1'"/>
   <rule key="{aa4cd2dc-685e-4569-b80c-07d00d90c7f4}" label="TC(2)" symbol="12" filter="&quot;defectType&quot; = 'TC' and &quot;severity&quot; = '2'"/>
   <rule key="{48acf436-056a-4c61-8d95-bef548561bf0}" label="TC(1)" symbol="13" filter="&quot;defectType&quot; = 'TC' and &quot;severity&quot; = '1'"/>
   <rule key="{395bde99-5f2c-489a-b36d-4b084bbf062e}" label="HFSC" symbol="14" filter="&quot;defectType&quot; = 'HFSC'"/>
   <rule key="{f0741863-47eb-466b-8ecc-3381620cec6c}" label="TSSC" symbol="15" filter="&quot;defectType&quot; = 'TSSC'"/>
   <rule key="{ed02eed5-3636-4f11-8fb3-c94690cf5859}" symbol="16" filter="ELSE"/>
  </rules>
  <symbols>
   <symbol name="0" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleLine" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="align_dash_pattern" type="QString" value="0"/>
      <Option name="capstyle" type="QString" value="square"/>
      <Option name="customdash" type="QString" value="5;2"/>
      <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="customdash_unit" type="QString" value="MM"/>
      <Option name="dash_pattern_offset" type="QString" value="0"/>
      <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
      <Option name="draw_inside_polygon" type="QString" value="0"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="line_color" type="QString" value="255,1,1,255"/>
      <Option name="line_style" type="QString" value="solid"/>
      <Option name="line_width" type="QString" value="0.26"/>
      <Option name="line_width_unit" type="QString" value="MM"/>
      <Option name="offset" type="QString" value="0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="ring_filter" type="QString" value="0"/>
      <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
      <Option name="use_custom_dash" type="QString" value="0"/>
      <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
     </Option>
     <prop v="0" k="align_dash_pattern"/>
     <prop v="square" k="capstyle"/>
     <prop v="5;2" k="customdash"/>
     <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
     <prop v="MM" k="customdash_unit"/>
     <prop v="0" k="dash_pattern_offset"/>
     <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
     <prop v="MM" k="dash_pattern_offset_unit"/>
     <prop v="0" k="draw_inside_polygon"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="255,1,1,255" k="line_color"/>
     <prop v="solid" k="line_style"/>
     <prop v="0.26" k="line_width"/>
     <prop v="MM" k="line_width_unit"/>
     <prop v="0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="0" k="ring_filter"/>
     <prop v="0" k="tweak_dash_pattern_on_corners"/>
     <prop v="0" k="use_custom_dash"/>
     <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
    <layer class="LinePatternFill" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="angle" type="QString" value="45"/>
      <Option name="color" type="QString" value="0,0,255,255"/>
      <Option name="distance" type="QString" value="5"/>
      <Option name="distance_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="distance_unit" type="QString" value="MM"/>
      <Option name="line_width" type="QString" value="0.26"/>
      <Option name="line_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="line_width_unit" type="QString" value="MM"/>
      <Option name="offset" type="QString" value="0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="outline_width_unit" type="QString" value="MM"/>
     </Option>
     <prop v="45" k="angle"/>
     <prop v="0,0,255,255" k="color"/>
     <prop v="5" k="distance"/>
     <prop v="3x:0,0,0,0,0,0" k="distance_map_unit_scale"/>
     <prop v="MM" k="distance_unit"/>
     <prop v="0.26" k="line_width"/>
     <prop v="3x:0,0,0,0,0,0" k="line_width_map_unit_scale"/>
     <prop v="MM" k="line_width_unit"/>
     <prop v="0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
     <prop v="MM" k="outline_width_unit"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
     <symbol name="@0@1" alpha="1" type="line" clip_to_extent="1" force_rhr="0">
      <data_defined_properties>
       <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
       </Option>
      </data_defined_properties>
      <layer class="SimpleLine" enabled="1" locked="0" pass="0">
       <Option type="Map">
        <Option name="align_dash_pattern" type="QString" value="0"/>
        <Option name="capstyle" type="QString" value="square"/>
        <Option name="customdash" type="QString" value="5;2"/>
        <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
        <Option name="customdash_unit" type="QString" value="MM"/>
        <Option name="dash_pattern_offset" type="QString" value="0"/>
        <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
        <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
        <Option name="draw_inside_polygon" type="QString" value="0"/>
        <Option name="joinstyle" type="QString" value="bevel"/>
        <Option name="line_color" type="QString" value="231,0,3,255"/>
        <Option name="line_style" type="QString" value="solid"/>
        <Option name="line_width" type="QString" value="0.26"/>
        <Option name="line_width_unit" type="QString" value="MM"/>
        <Option name="offset" type="QString" value="0"/>
        <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
        <Option name="offset_unit" type="QString" value="MM"/>
        <Option name="ring_filter" type="QString" value="0"/>
        <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
        <Option name="use_custom_dash" type="QString" value="0"/>
        <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
       </Option>
       <prop v="0" k="align_dash_pattern"/>
       <prop v="square" k="capstyle"/>
       <prop v="5;2" k="customdash"/>
       <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
       <prop v="MM" k="customdash_unit"/>
       <prop v="0" k="dash_pattern_offset"/>
       <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
       <prop v="MM" k="dash_pattern_offset_unit"/>
       <prop v="0" k="draw_inside_polygon"/>
       <prop v="bevel" k="joinstyle"/>
       <prop v="231,0,3,255" k="line_color"/>
       <prop v="solid" k="line_style"/>
       <prop v="0.26" k="line_width"/>
       <prop v="MM" k="line_width_unit"/>
       <prop v="0" k="offset"/>
       <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
       <prop v="MM" k="offset_unit"/>
       <prop v="0" k="ring_filter"/>
       <prop v="0" k="tweak_dash_pattern_on_corners"/>
       <prop v="0" k="use_custom_dash"/>
       <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
       <data_defined_properties>
        <Option type="Map">
         <Option name="name" type="QString" value=""/>
         <Option name="properties"/>
         <Option name="type" type="QString" value="collection"/>
        </Option>
       </data_defined_properties>
      </layer>
     </symbol>
    </layer>
   </symbol>
   <symbol name="1" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleLine" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="align_dash_pattern" type="QString" value="0"/>
      <Option name="capstyle" type="QString" value="square"/>
      <Option name="customdash" type="QString" value="5;2"/>
      <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="customdash_unit" type="QString" value="MM"/>
      <Option name="dash_pattern_offset" type="QString" value="0"/>
      <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
      <Option name="draw_inside_polygon" type="QString" value="0"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="line_color" type="QString" value="255,1,1,255"/>
      <Option name="line_style" type="QString" value="dot"/>
      <Option name="line_width" type="QString" value="0.26"/>
      <Option name="line_width_unit" type="QString" value="MM"/>
      <Option name="offset" type="QString" value="0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="ring_filter" type="QString" value="0"/>
      <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
      <Option name="use_custom_dash" type="QString" value="0"/>
      <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
     </Option>
     <prop v="0" k="align_dash_pattern"/>
     <prop v="square" k="capstyle"/>
     <prop v="5;2" k="customdash"/>
     <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
     <prop v="MM" k="customdash_unit"/>
     <prop v="0" k="dash_pattern_offset"/>
     <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
     <prop v="MM" k="dash_pattern_offset_unit"/>
     <prop v="0" k="draw_inside_polygon"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="255,1,1,255" k="line_color"/>
     <prop v="dot" k="line_style"/>
     <prop v="0.26" k="line_width"/>
     <prop v="MM" k="line_width_unit"/>
     <prop v="0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="0" k="ring_filter"/>
     <prop v="0" k="tweak_dash_pattern_on_corners"/>
     <prop v="0" k="use_custom_dash"/>
     <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
    <layer class="LinePatternFill" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="angle" type="QString" value="-45"/>
      <Option name="color" type="QString" value="0,0,255,255"/>
      <Option name="distance" type="QString" value="5"/>
      <Option name="distance_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="distance_unit" type="QString" value="MM"/>
      <Option name="line_width" type="QString" value="0.26"/>
      <Option name="line_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="line_width_unit" type="QString" value="MM"/>
      <Option name="offset" type="QString" value="0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="outline_width_unit" type="QString" value="MM"/>
     </Option>
     <prop v="-45" k="angle"/>
     <prop v="0,0,255,255" k="color"/>
     <prop v="5" k="distance"/>
     <prop v="3x:0,0,0,0,0,0" k="distance_map_unit_scale"/>
     <prop v="MM" k="distance_unit"/>
     <prop v="0.26" k="line_width"/>
     <prop v="3x:0,0,0,0,0,0" k="line_width_map_unit_scale"/>
     <prop v="MM" k="line_width_unit"/>
     <prop v="0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
     <prop v="MM" k="outline_width_unit"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
     <symbol name="@1@1" alpha="1" type="line" clip_to_extent="1" force_rhr="0">
      <data_defined_properties>
       <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
       </Option>
      </data_defined_properties>
      <layer class="SimpleLine" enabled="1" locked="0" pass="0">
       <Option type="Map">
        <Option name="align_dash_pattern" type="QString" value="0"/>
        <Option name="capstyle" type="QString" value="square"/>
        <Option name="customdash" type="QString" value="5;2"/>
        <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
        <Option name="customdash_unit" type="QString" value="MM"/>
        <Option name="dash_pattern_offset" type="QString" value="0"/>
        <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
        <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
        <Option name="draw_inside_polygon" type="QString" value="0"/>
        <Option name="joinstyle" type="QString" value="bevel"/>
        <Option name="line_color" type="QString" value="231,0,3,255"/>
        <Option name="line_style" type="QString" value="dash"/>
        <Option name="line_width" type="QString" value="0.26"/>
        <Option name="line_width_unit" type="QString" value="MM"/>
        <Option name="offset" type="QString" value="0"/>
        <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
        <Option name="offset_unit" type="QString" value="MM"/>
        <Option name="ring_filter" type="QString" value="0"/>
        <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
        <Option name="use_custom_dash" type="QString" value="0"/>
        <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
       </Option>
       <prop v="0" k="align_dash_pattern"/>
       <prop v="square" k="capstyle"/>
       <prop v="5;2" k="customdash"/>
       <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
       <prop v="MM" k="customdash_unit"/>
       <prop v="0" k="dash_pattern_offset"/>
       <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
       <prop v="MM" k="dash_pattern_offset_unit"/>
       <prop v="0" k="draw_inside_polygon"/>
       <prop v="bevel" k="joinstyle"/>
       <prop v="231,0,3,255" k="line_color"/>
       <prop v="dash" k="line_style"/>
       <prop v="0.26" k="line_width"/>
       <prop v="MM" k="line_width_unit"/>
       <prop v="0" k="offset"/>
       <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
       <prop v="MM" k="offset_unit"/>
       <prop v="0" k="ring_filter"/>
       <prop v="0" k="tweak_dash_pattern_on_corners"/>
       <prop v="0" k="use_custom_dash"/>
       <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
       <data_defined_properties>
        <Option type="Map">
         <Option name="name" type="QString" value=""/>
         <Option name="properties"/>
         <Option name="type" type="QString" value="collection"/>
        </Option>
       </data_defined_properties>
      </layer>
     </symbol>
    </layer>
   </symbol>
   <symbol name="10" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleFill" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="border_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="color" type="QString" value="246,0,234,255"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="offset" type="QString" value="0,0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="outline_color" type="QString" value="35,35,35,255"/>
      <Option name="outline_style" type="QString" value="solid"/>
      <Option name="outline_width" type="QString" value="0.26"/>
      <Option name="outline_width_unit" type="QString" value="MM"/>
      <Option name="style" type="QString" value="solid"/>
     </Option>
     <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
     <prop v="246,0,234,255" k="color"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="0,0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="35,35,35,255" k="outline_color"/>
     <prop v="solid" k="outline_style"/>
     <prop v="0.26" k="outline_width"/>
     <prop v="MM" k="outline_width_unit"/>
     <prop v="solid" k="style"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="11" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleFill" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="border_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="color" type="QString" value="243,166,178,255"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="offset" type="QString" value="0,0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="outline_color" type="QString" value="35,35,35,255"/>
      <Option name="outline_style" type="QString" value="solid"/>
      <Option name="outline_width" type="QString" value="0.26"/>
      <Option name="outline_width_unit" type="QString" value="MM"/>
      <Option name="style" type="QString" value="solid"/>
     </Option>
     <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
     <prop v="243,166,178,255" k="color"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="0,0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="35,35,35,255" k="outline_color"/>
     <prop v="solid" k="outline_style"/>
     <prop v="0.26" k="outline_width"/>
     <prop v="MM" k="outline_width_unit"/>
     <prop v="solid" k="style"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="12" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleLine" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="align_dash_pattern" type="QString" value="0"/>
      <Option name="capstyle" type="QString" value="square"/>
      <Option name="customdash" type="QString" value="5;2"/>
      <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="customdash_unit" type="QString" value="MM"/>
      <Option name="dash_pattern_offset" type="QString" value="0"/>
      <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
      <Option name="draw_inside_polygon" type="QString" value="0"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="line_color" type="QString" value="231,0,3,255"/>
      <Option name="line_style" type="QString" value="solid"/>
      <Option name="line_width" type="QString" value="0.26"/>
      <Option name="line_width_unit" type="QString" value="MM"/>
      <Option name="offset" type="QString" value="0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="ring_filter" type="QString" value="0"/>
      <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
      <Option name="use_custom_dash" type="QString" value="0"/>
      <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
     </Option>
     <prop v="0" k="align_dash_pattern"/>
     <prop v="square" k="capstyle"/>
     <prop v="5;2" k="customdash"/>
     <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
     <prop v="MM" k="customdash_unit"/>
     <prop v="0" k="dash_pattern_offset"/>
     <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
     <prop v="MM" k="dash_pattern_offset_unit"/>
     <prop v="0" k="draw_inside_polygon"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="231,0,3,255" k="line_color"/>
     <prop v="solid" k="line_style"/>
     <prop v="0.26" k="line_width"/>
     <prop v="MM" k="line_width_unit"/>
     <prop v="0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="0" k="ring_filter"/>
     <prop v="0" k="tweak_dash_pattern_on_corners"/>
     <prop v="0" k="use_custom_dash"/>
     <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="13" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleLine" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="align_dash_pattern" type="QString" value="0"/>
      <Option name="capstyle" type="QString" value="square"/>
      <Option name="customdash" type="QString" value="5;2"/>
      <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="customdash_unit" type="QString" value="MM"/>
      <Option name="dash_pattern_offset" type="QString" value="0"/>
      <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
      <Option name="draw_inside_polygon" type="QString" value="0"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="line_color" type="QString" value="231,0,3,255"/>
      <Option name="line_style" type="QString" value="dash"/>
      <Option name="line_width" type="QString" value="0.26"/>
      <Option name="line_width_unit" type="QString" value="MM"/>
      <Option name="offset" type="QString" value="0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="ring_filter" type="QString" value="0"/>
      <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
      <Option name="use_custom_dash" type="QString" value="0"/>
      <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
     </Option>
     <prop v="0" k="align_dash_pattern"/>
     <prop v="square" k="capstyle"/>
     <prop v="5;2" k="customdash"/>
     <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
     <prop v="MM" k="customdash_unit"/>
     <prop v="0" k="dash_pattern_offset"/>
     <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
     <prop v="MM" k="dash_pattern_offset_unit"/>
     <prop v="0" k="draw_inside_polygon"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="231,0,3,255" k="line_color"/>
     <prop v="dash" k="line_style"/>
     <prop v="0.26" k="line_width"/>
     <prop v="MM" k="line_width_unit"/>
     <prop v="0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="0" k="ring_filter"/>
     <prop v="0" k="tweak_dash_pattern_on_corners"/>
     <prop v="0" k="use_custom_dash"/>
     <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="14" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleFill" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="border_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="color" type="QString" value="150,150,150,255"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="offset" type="QString" value="0,0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="outline_color" type="QString" value="247,247,247,255"/>
      <Option name="outline_style" type="QString" value="solid"/>
      <Option name="outline_width" type="QString" value="0.26"/>
      <Option name="outline_width_unit" type="QString" value="MM"/>
      <Option name="style" type="QString" value="solid"/>
     </Option>
     <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
     <prop v="150,150,150,255" k="color"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="0,0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="247,247,247,255" k="outline_color"/>
     <prop v="solid" k="outline_style"/>
     <prop v="0.26" k="outline_width"/>
     <prop v="MM" k="outline_width_unit"/>
     <prop v="solid" k="style"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="15" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleFill" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="border_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="color" type="QString" value="150,150,150,255"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="offset" type="QString" value="0,0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="outline_color" type="QString" value="247,247,247,255"/>
      <Option name="outline_style" type="QString" value="solid"/>
      <Option name="outline_width" type="QString" value="0.26"/>
      <Option name="outline_width_unit" type="QString" value="MM"/>
      <Option name="style" type="QString" value="solid"/>
     </Option>
     <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
     <prop v="150,150,150,255" k="color"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="0,0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="247,247,247,255" k="outline_color"/>
     <prop v="solid" k="outline_style"/>
     <prop v="0.26" k="outline_width"/>
     <prop v="MM" k="outline_width_unit"/>
     <prop v="solid" k="style"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="16" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleFill" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="border_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="color" type="QString" value="122,4,3,255"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="offset" type="QString" value="0,0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="outline_color" type="QString" value="35,35,35,255"/>
      <Option name="outline_style" type="QString" value="solid"/>
      <Option name="outline_width" type="QString" value="0.26"/>
      <Option name="outline_width_unit" type="QString" value="MM"/>
      <Option name="style" type="QString" value="solid"/>
     </Option>
     <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
     <prop v="122,4,3,255" k="color"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="0,0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="35,35,35,255" k="outline_color"/>
     <prop v="solid" k="outline_style"/>
     <prop v="0.26" k="outline_width"/>
     <prop v="MM" k="outline_width_unit"/>
     <prop v="solid" k="style"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="2" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleFill" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="border_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="color" type="QString" value="250,209,2,255"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="offset" type="QString" value="0,0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="outline_color" type="QString" value="35,35,35,255"/>
      <Option name="outline_style" type="QString" value="solid"/>
      <Option name="outline_width" type="QString" value="0.26"/>
      <Option name="outline_width_unit" type="QString" value="MM"/>
      <Option name="style" type="QString" value="solid"/>
     </Option>
     <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
     <prop v="250,209,2,255" k="color"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="0,0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="35,35,35,255" k="outline_color"/>
     <prop v="solid" k="outline_style"/>
     <prop v="0.26" k="outline_width"/>
     <prop v="MM" k="outline_width_unit"/>
     <prop v="solid" k="style"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="3" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleFill" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="border_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="color" type="QString" value="252,154,26,255"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="offset" type="QString" value="0,0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="outline_color" type="QString" value="35,35,35,255"/>
      <Option name="outline_style" type="QString" value="solid"/>
      <Option name="outline_width" type="QString" value="0.26"/>
      <Option name="outline_width_unit" type="QString" value="MM"/>
      <Option name="style" type="QString" value="solid"/>
     </Option>
     <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
     <prop v="252,154,26,255" k="color"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="0,0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="35,35,35,255" k="outline_color"/>
     <prop v="solid" k="outline_style"/>
     <prop v="0.26" k="outline_width"/>
     <prop v="MM" k="outline_width_unit"/>
     <prop v="solid" k="style"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="4" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleLine" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="align_dash_pattern" type="QString" value="0"/>
      <Option name="capstyle" type="QString" value="square"/>
      <Option name="customdash" type="QString" value="5;2"/>
      <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="customdash_unit" type="QString" value="MM"/>
      <Option name="dash_pattern_offset" type="QString" value="0"/>
      <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
      <Option name="draw_inside_polygon" type="QString" value="0"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="line_color" type="QString" value="35,35,35,255"/>
      <Option name="line_style" type="QString" value="dot"/>
      <Option name="line_width" type="QString" value="1.86"/>
      <Option name="line_width_unit" type="QString" value="MM"/>
      <Option name="offset" type="QString" value="0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="ring_filter" type="QString" value="0"/>
      <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
      <Option name="use_custom_dash" type="QString" value="0"/>
      <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
     </Option>
     <prop v="0" k="align_dash_pattern"/>
     <prop v="square" k="capstyle"/>
     <prop v="5;2" k="customdash"/>
     <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
     <prop v="MM" k="customdash_unit"/>
     <prop v="0" k="dash_pattern_offset"/>
     <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
     <prop v="MM" k="dash_pattern_offset_unit"/>
     <prop v="0" k="draw_inside_polygon"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="35,35,35,255" k="line_color"/>
     <prop v="dot" k="line_style"/>
     <prop v="1.86" k="line_width"/>
     <prop v="MM" k="line_width_unit"/>
     <prop v="0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="0" k="ring_filter"/>
     <prop v="0" k="tweak_dash_pattern_on_corners"/>
     <prop v="0" k="use_custom_dash"/>
     <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="5" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleLine" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="align_dash_pattern" type="QString" value="0"/>
      <Option name="capstyle" type="QString" value="square"/>
      <Option name="customdash" type="QString" value="5;2"/>
      <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="customdash_unit" type="QString" value="MM"/>
      <Option name="dash_pattern_offset" type="QString" value="0"/>
      <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
      <Option name="draw_inside_polygon" type="QString" value="0"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="line_color" type="QString" value="4,249,21,255"/>
      <Option name="line_style" type="QString" value="solid"/>
      <Option name="line_width" type="QString" value="0.26"/>
      <Option name="line_width_unit" type="QString" value="MM"/>
      <Option name="offset" type="QString" value="0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="ring_filter" type="QString" value="0"/>
      <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
      <Option name="use_custom_dash" type="QString" value="0"/>
      <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
     </Option>
     <prop v="0" k="align_dash_pattern"/>
     <prop v="square" k="capstyle"/>
     <prop v="5;2" k="customdash"/>
     <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
     <prop v="MM" k="customdash_unit"/>
     <prop v="0" k="dash_pattern_offset"/>
     <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
     <prop v="MM" k="dash_pattern_offset_unit"/>
     <prop v="0" k="draw_inside_polygon"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="4,249,21,255" k="line_color"/>
     <prop v="solid" k="line_style"/>
     <prop v="0.26" k="line_width"/>
     <prop v="MM" k="line_width_unit"/>
     <prop v="0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="0" k="ring_filter"/>
     <prop v="0" k="tweak_dash_pattern_on_corners"/>
     <prop v="0" k="use_custom_dash"/>
     <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="6" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleLine" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="align_dash_pattern" type="QString" value="0"/>
      <Option name="capstyle" type="QString" value="square"/>
      <Option name="customdash" type="QString" value="5;2"/>
      <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="customdash_unit" type="QString" value="MM"/>
      <Option name="dash_pattern_offset" type="QString" value="0"/>
      <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
      <Option name="draw_inside_polygon" type="QString" value="0"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="line_color" type="QString" value="231,0,3,255"/>
      <Option name="line_style" type="QString" value="solid"/>
      <Option name="line_width" type="QString" value="0.46"/>
      <Option name="line_width_unit" type="QString" value="MM"/>
      <Option name="offset" type="QString" value="0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="ring_filter" type="QString" value="0"/>
      <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
      <Option name="use_custom_dash" type="QString" value="0"/>
      <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
     </Option>
     <prop v="0" k="align_dash_pattern"/>
     <prop v="square" k="capstyle"/>
     <prop v="5;2" k="customdash"/>
     <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
     <prop v="MM" k="customdash_unit"/>
     <prop v="0" k="dash_pattern_offset"/>
     <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
     <prop v="MM" k="dash_pattern_offset_unit"/>
     <prop v="0" k="draw_inside_polygon"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="231,0,3,255" k="line_color"/>
     <prop v="solid" k="line_style"/>
     <prop v="0.46" k="line_width"/>
     <prop v="MM" k="line_width_unit"/>
     <prop v="0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="0" k="ring_filter"/>
     <prop v="0" k="tweak_dash_pattern_on_corners"/>
     <prop v="0" k="use_custom_dash"/>
     <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="7" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleLine" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="align_dash_pattern" type="QString" value="0"/>
      <Option name="capstyle" type="QString" value="square"/>
      <Option name="customdash" type="QString" value="5;2"/>
      <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="customdash_unit" type="QString" value="MM"/>
      <Option name="dash_pattern_offset" type="QString" value="0"/>
      <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
      <Option name="draw_inside_polygon" type="QString" value="0"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="line_color" type="QString" value="231,0,3,255"/>
      <Option name="line_style" type="QString" value="solid"/>
      <Option name="line_width" type="QString" value="2.26"/>
      <Option name="line_width_unit" type="QString" value="MM"/>
      <Option name="offset" type="QString" value="0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="ring_filter" type="QString" value="0"/>
      <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
      <Option name="use_custom_dash" type="QString" value="0"/>
      <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
     </Option>
     <prop v="0" k="align_dash_pattern"/>
     <prop v="square" k="capstyle"/>
     <prop v="5;2" k="customdash"/>
     <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
     <prop v="MM" k="customdash_unit"/>
     <prop v="0" k="dash_pattern_offset"/>
     <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
     <prop v="MM" k="dash_pattern_offset_unit"/>
     <prop v="0" k="draw_inside_polygon"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="231,0,3,255" k="line_color"/>
     <prop v="solid" k="line_style"/>
     <prop v="2.26" k="line_width"/>
     <prop v="MM" k="line_width_unit"/>
     <prop v="0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="0" k="ring_filter"/>
     <prop v="0" k="tweak_dash_pattern_on_corners"/>
     <prop v="0" k="use_custom_dash"/>
     <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol name="8" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleFill" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="border_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="color" type="QString" value="255,255,255,255"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="offset" type="QString" value="0,0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="outline_color" type="QString" value="35,35,35,255"/>
      <Option name="outline_style" type="QString" value="solid"/>
      <Option name="outline_width" type="QString" value="0.26"/>
      <Option name="outline_width_unit" type="QString" value="MM"/>
      <Option name="style" type="QString" value="solid"/>
     </Option>
     <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
     <prop v="255,255,255,255" k="color"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="0,0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="35,35,35,255" k="outline_color"/>
     <prop v="solid" k="outline_style"/>
     <prop v="0.26" k="outline_width"/>
     <prop v="MM" k="outline_width_unit"/>
     <prop v="solid" k="style"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
    <layer class="LinePatternFill" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="angle" type="QString" value="45"/>
      <Option name="color" type="QString" value="255,255,255,255"/>
      <Option name="distance" type="QString" value="2.4"/>
      <Option name="distance_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="distance_unit" type="QString" value="MM"/>
      <Option name="line_width" type="QString" value="0.26"/>
      <Option name="line_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="line_width_unit" type="QString" value="MM"/>
      <Option name="offset" type="QString" value="0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="outline_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="outline_width_unit" type="QString" value="MM"/>
     </Option>
     <prop v="45" k="angle"/>
     <prop v="255,255,255,255" k="color"/>
     <prop v="2.4" k="distance"/>
     <prop v="3x:0,0,0,0,0,0" k="distance_map_unit_scale"/>
     <prop v="MM" k="distance_unit"/>
     <prop v="0.26" k="line_width"/>
     <prop v="3x:0,0,0,0,0,0" k="line_width_map_unit_scale"/>
     <prop v="MM" k="line_width_unit"/>
     <prop v="0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
     <prop v="MM" k="outline_width_unit"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
     <symbol name="@8@1" alpha="1" type="line" clip_to_extent="1" force_rhr="0">
      <data_defined_properties>
       <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
       </Option>
      </data_defined_properties>
      <layer class="SimpleLine" enabled="1" locked="0" pass="0">
       <Option type="Map">
        <Option name="align_dash_pattern" type="QString" value="0"/>
        <Option name="capstyle" type="QString" value="square"/>
        <Option name="customdash" type="QString" value="5;2"/>
        <Option name="customdash_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
        <Option name="customdash_unit" type="QString" value="MM"/>
        <Option name="dash_pattern_offset" type="QString" value="0"/>
        <Option name="dash_pattern_offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
        <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
        <Option name="draw_inside_polygon" type="QString" value="0"/>
        <Option name="joinstyle" type="QString" value="bevel"/>
        <Option name="line_color" type="QString" value="1,98,255,255"/>
        <Option name="line_style" type="QString" value="solid"/>
        <Option name="line_width" type="QString" value="0.26"/>
        <Option name="line_width_unit" type="QString" value="MM"/>
        <Option name="offset" type="QString" value="0"/>
        <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
        <Option name="offset_unit" type="QString" value="MM"/>
        <Option name="ring_filter" type="QString" value="0"/>
        <Option name="tweak_dash_pattern_on_corners" type="QString" value="0"/>
        <Option name="use_custom_dash" type="QString" value="0"/>
        <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
       </Option>
       <prop v="0" k="align_dash_pattern"/>
       <prop v="square" k="capstyle"/>
       <prop v="5;2" k="customdash"/>
       <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
       <prop v="MM" k="customdash_unit"/>
       <prop v="0" k="dash_pattern_offset"/>
       <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
       <prop v="MM" k="dash_pattern_offset_unit"/>
       <prop v="0" k="draw_inside_polygon"/>
       <prop v="bevel" k="joinstyle"/>
       <prop v="1,98,255,255" k="line_color"/>
       <prop v="solid" k="line_style"/>
       <prop v="0.26" k="line_width"/>
       <prop v="MM" k="line_width_unit"/>
       <prop v="0" k="offset"/>
       <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
       <prop v="MM" k="offset_unit"/>
       <prop v="0" k="ring_filter"/>
       <prop v="0" k="tweak_dash_pattern_on_corners"/>
       <prop v="0" k="use_custom_dash"/>
       <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
       <data_defined_properties>
        <Option type="Map">
         <Option name="name" type="QString" value=""/>
         <Option name="properties"/>
         <Option name="type" type="QString" value="collection"/>
        </Option>
       </data_defined_properties>
      </layer>
     </symbol>
    </layer>
   </symbol>
   <symbol name="9" alpha="1" type="fill" clip_to_extent="1" force_rhr="0">
    <data_defined_properties>
     <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
     </Option>
    </data_defined_properties>
    <layer class="SimpleFill" enabled="1" locked="0" pass="0">
     <Option type="Map">
      <Option name="border_width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="color" type="QString" value="0,0,0,255"/>
      <Option name="joinstyle" type="QString" value="bevel"/>
      <Option name="offset" type="QString" value="0,0"/>
      <Option name="offset_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
      <Option name="offset_unit" type="QString" value="MM"/>
      <Option name="outline_color" type="QString" value="35,35,35,255"/>
      <Option name="outline_style" type="QString" value="solid"/>
      <Option name="outline_width" type="QString" value="0.26"/>
      <Option name="outline_width_unit" type="QString" value="MM"/>
      <Option name="style" type="QString" value="solid"/>
     </Option>
     <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
     <prop v="0,0,0,255" k="color"/>
     <prop v="bevel" k="joinstyle"/>
     <prop v="0,0" k="offset"/>
     <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
     <prop v="MM" k="offset_unit"/>
     <prop v="35,35,35,255" k="outline_color"/>
     <prop v="solid" k="outline_style"/>
     <prop v="0.26" k="outline_width"/>
     <prop v="MM" k="outline_width_unit"/>
     <prop v="solid" k="style"/>
     <data_defined_properties>
      <Option type="Map">
       <Option name="name" type="QString" value=""/>
       <Option name="properties"/>
       <Option name="type" type="QString" value="collection"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
  </symbols>
 </renderer-v2>
 <blendMode>0</blendMode>
 <featureBlendMode>0</featureBlendMode>
 <layerGeometryType>2</layerGeometryType>
</qgis>
