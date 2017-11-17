
@implementation testVC2

- (void)viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:animated];
}
- (void)viewDidLoad {
    [super viewDidLoad];
    
    [ApplicationDelegate uploadUserStartAction:@"商品详情adfadf" Sellerid:@"" URLString:KXiaoNengGoodsInfo];
}

- (void)viewWillAppear:(BOOL)animated
{
    [super viewWillAppear:animated];

    [MobClick beginLogPageView:@"产品详情页面"];

    [TalkingData trackPageBegin:@"产品详情页面"];

}

- (void)viewWillDisappear:(BOOL)animated
{
    [super viewWillDisappear:animated];
}

- (void)testfunction
{
    //@"产品详情页面 1"
    NSLog(@"产品详情页面 2")
    favoriteLabel.text = @"已收藏adf";
}

@end
