(set-logic ALL)
; Frontier Constraint ID: c09788fd597a0140
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1039)) (False)
(assert (not (= x 1039)))

; Query: ((== x 1040)) (False)
(assert (not (not (= x 1040))))

(check-sat)
(get-model)
