(set-logic ALL)
; Frontier Constraint ID: 1b78cbcfaacdd11a
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 427)) (False)
(assert (not (= x 427)))

; Query: ((== x 428)) (False)
(assert (not (not (= x 428))))

(check-sat)
(get-model)
