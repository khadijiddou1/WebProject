import 'package:flutter/material.dart';
import 'package:projectlben/services/api_service.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final ApiService _apiService = ApiService();
  Map<String, dynamic>? _userProfile;
  List<dynamic> _products = [];
  List<dynamic> _orders = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      final profile = await _apiService.getUserProfile();
      final products = await _apiService.getProducts();
      final orders = await _apiService.getOrders();

      setState(() {
        _userProfile = profile;
        _products = products;
        _orders = orders;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to load data: ${e.toString()}')),
      );
    }
  }

  Future<void> _logout() async {
    Navigator.pushReplacementNamed(context, '/login');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Welcome ${_userProfile?['username'] ?? ''}'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : DefaultTabController(
              length: 2,
              child: Column(
                children: [
                  const TabBar(
                    tabs: [
                      Tab(text: 'Products'),
                      Tab(text: 'Orders'),
                    ],
                  ),
                  Expanded(
                    child: TabBarView(
                      children: [
                        // Products Tab
                        ListView.builder(
                          itemCount: _products.length,
                          itemBuilder: (context, index) {
                            final product = _products[index];
                            return ListTile(
                              title: Text(product['nom']),
                              subtitle: Text('\$${product['prix']}'),
                            );
                          },
                        ),
                        // Orders Tab
                        ListView.builder(
                          itemCount: _orders.length,
                          itemBuilder: (context, index) {
                            final order = _orders[index];
                            return ListTile(
                              title: Text(order['produit']['nom']),
                              subtitle: Text('Status: ${order['statut']}'),
                              trailing: Text('\$${order['montant_total']}'),
                            );
                          },
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}