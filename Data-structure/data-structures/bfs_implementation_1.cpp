// MAT_ShortestDistBtw2CellsMat.cpp
//
/*
	Author: HitmanM3nace
	@ayusofayush
	Date: 16 June 2019
	Prob.: Shortest Distance From Src to Dest.
	Approach: BFS
	TC: O(n+m)
*/

#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define fast ios::sync_with_stdio(false);cin.tie(0);cout.tie(0);
#define fr(i,n) for(int i=0;i<n;i++)
#define fnr(i,a,b) for(int i=a;i<b;i++)
#define pb push_back
#define F first
#define S second
#define sz(arr) sizeof(arr)/sizeof(arr[0])

const int mx2 = 1e6+5;
int dist[100][100];
int n,m;
int dx[] = {1,0,-1,0};
int dy[] = {0,1,0,-1};

bool isvalid(char grid[][100],int x,int y) {
	return x>=0 && y>=0 && x<n && y<m && grid[x][y]!='0';
}

int minDist(char grid[][100],int i,int j) {
	queue<pair<int,int>> q;
	q.push({i,j});
	dist[i][j] = 0;
	while(!q.empty()) {
		i = q.front().F;
		j = q.front().S;
		if(grid[i][j]=='d') 
			return dist[i][j];
		q.pop();
		for(int k=0;k<4;k++) {
			int u = i+dx[k];
			int v = j+dy[k];
			if(isvalid(grid,u,v)) {
				if(dist[u][v]==-1) {
					dist[u][v] = dist[i][j] + 1;
					q.push({u,v});
				}
			}
		}
	}
	return -1;
}

int main() {
	n = 4,m=4;
	char grid[100][100] = { { '0', '*', '0', 's' }, 
                        { '*', '0', '*', '*' }, 
                        { '0', '*', '*', '*' }, 
                        { 'd', '*', '*', '*' } }; 	
	memset(dist,-1,sizeof dist);
	cout<<minDist(grid,0,3)<<endl;
	return 0;
}
