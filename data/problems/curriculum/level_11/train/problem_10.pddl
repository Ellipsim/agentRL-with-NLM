

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on-table b1)
(on b2 b5)
(on b3 b10)
(on b4 b3)
(on b5 b9)
(on b6 b2)
(on-table b7)
(on b8 b7)
(on b9 b11)
(on b10 b6)
(on-table b11)
(on-table b12)
(clear b1)
(clear b4)
(clear b8)
(clear b12)
)
(:goal
(and
(on b1 b10)
(on b4 b6)
(on b6 b1)
(on b7 b8)
(on b9 b7)
(on b10 b9)
(on b11 b2))
)
)


