

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on-table b1)
(on b2 b3)
(on b3 b12)
(on b4 b2)
(on b5 b1)
(on b6 b10)
(on b7 b9)
(on b8 b6)
(on-table b9)
(on-table b10)
(on b11 b4)
(on b12 b7)
(clear b5)
(clear b8)
(clear b11)
)
(:goal
(and
(on b1 b3)
(on b4 b12)
(on b5 b4)
(on b6 b2)
(on b7 b11)
(on b8 b9)
(on b10 b8)
(on b11 b10))
)
)


