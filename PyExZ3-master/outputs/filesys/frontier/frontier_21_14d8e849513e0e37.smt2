(set-logic ALL)
; Frontier Constraint ID: 14d8e849513e0e37
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1342)) (False)
(assert (not (= x 1342)))

; Query: ((== x 1343)) (False)
(assert (not (not (= x 1343))))

(check-sat)
(get-model)
