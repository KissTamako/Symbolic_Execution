(set-logic ALL)
; Frontier Constraint ID: d5a67286efa17601
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 562)) (False)
(assert (not (= x 562)))

; Query: ((== x 563)) (False)
(assert (not (not (= x 563))))

(check-sat)
(get-model)
