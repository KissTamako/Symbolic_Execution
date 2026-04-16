(set-logic ALL)
; Frontier Constraint ID: e5bfcc7fdbde2179
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 433)) (False)
(assert (not (not (= x 433))))

(check-sat)
(get-model)
