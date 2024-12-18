const am5Ready = () => new Promise((resolve) => {
  am5.ready(resolve); // am5.ready()가 완료되면 resolve 호출
});


// const id = new URLSearchParams(window.location.search).get('id');
// const fetchSummary = () => fetch(`https://code.changoo.site/api/summary?id=${id}`)
// .then((response) => {
//   if (!response.ok) {
//     throw new Error("Network response was not ok " + response.statusText);
//   }
//   return response.json(); // JSON 데이터를 파싱
// });

// Promise.all([am5Ready(), fetchSummary()])
Promise.all([am5Ready()])
  .then(([_, response]) => {
    // const summary = response.summary;
    const summary = `댓글을 종합해보면, 대다수의 사용자들은 관세 전쟁에 대한 강한 관심을 보이고 있습니다. 중국과 미국 사이의 팽팽한 관계와 이에 따른 한국의 위치나 대응에 대한 궁금증을 표출하고 있습니다. 그 중에서도 특히 미국과 중국 간의 관세 전쟁과 세계 경제에 미칠 영향에 대한 우려의 목소리가 높습니다. 
    계엄령에 대한 댓글들은 비판적인 의견과 함께 그 효과와 영향에 대한 고민을 드러내며, 영상이 계엄령에 대해서 충분한 의견을 내지 않았음을 지적하고 있습니다. 또 다른 화제로는 '라이브'가 주목받았는데, 이에 대한 댓글들은 대체로 긍정적이며 사용자들의 높은 관심과 기대감을 확인할 수 있습니다. 사용자들은 특정 주제에 대해 심도있는 토론을 기대하고 있고 이 플랫폼에 대한 강한 참여 의사와 함께 인포테인먼트 콘텐츠에 대한 필요성을 주장하고 있습니다.`
    // const data = {
    //   value: 0,
    //   children: response.clusters.map((cluster) => ({value: 10, name: cluster}))
    // };
    const data = {
      value: 0,
      children:[
        {
          value: 80, 
          name: "관세전쟁",
          children: [

          ]
        },
        {
          value: 80, 
          name: "계엄령",
          children: [
            
          ]
        },
        {
          value: 50, 
          name: "미국",
          children: [
            
          ]
        },
        {
          value: 30, 
          name: "라이브",
          children: [
            
          ]
        },
      ]
    }

    const SummaryText = document.getElementById("text");
    SummaryText.innerHTML = summary;

    const root = am5.Root.new("chartdiv");
    root.setThemes([
      am5themes_Animated.new(root)
    ]);
  
    const container = root.container.children.push(am5.Container.new(root, {
      width: am5.percent(100),
      height: am5.percent(55),
      layout: root.verticalLayout
    }));
  
    const series = container.children.push(am5hierarchy.ForceDirected.new(root, {
      singleBranchOnly: false,
      downDepth: 2,
      topDepth: 1,
      initialDepth: 1,
      valueField: "value",
      categoryField: "name",
      childDataField: "children",
      idField: "name",
      linkWithField: "linkWith",
      manyBodyStrength: -10,
      centerStrength: 0.8
    }));
  
    series.get("colors").setAll({step: 2});
    series.links.template.set("strength", 0.5);
    series.data.setAll([data]);
    series.set("selectedDataItem", series.dataItems[0]);
    series.appear(1000, 100);

}).catch((error) => {
  console.error(error);
});
