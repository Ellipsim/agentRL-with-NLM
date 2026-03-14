

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b5)
(on b2 b11)
(on b3 b9)
(on b4 b3)
(on b5 b12)
(on-table b6)
(on-table b7)
(on b8 b10)
(on b9 b2)
(on-table b10)
(on b11 b8)
(on b12 b13)
(on-table b13)
(clear b1)
(clear b4)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b8)
(on b2 b10)
(on b3 b9)
(on b7 b2)
(on b9 b1)
(on b11 b5)
(on b12 b3)
(on b13 b4))
)
)


