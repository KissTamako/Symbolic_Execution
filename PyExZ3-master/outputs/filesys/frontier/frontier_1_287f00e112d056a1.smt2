(set-logic ALL)
; Frontier Constraint ID: 287f00e112d056a1
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 637)) (False)
(assert (not (= x 637)))

; Query: ((== x 638)) (False)
(assert (not (not (= x 638))))

(check-sat)
(get-model)
