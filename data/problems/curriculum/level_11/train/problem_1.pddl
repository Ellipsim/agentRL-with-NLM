

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b7)
(on b2 b5)
(on b3 b9)
(on-table b4)
(on b5 b12)
(on-table b6)
(on b7 b10)
(on-table b8)
(on-table b9)
(on-table b10)
(on b11 b6)
(on b12 b3)
(clear b1)
(clear b2)
(clear b4)
(clear b8)
(clear b11)
)
(:goal
(and
(on b1 b6)
(on b5 b7)
(on b6 b3)
(on b7 b10)
(on b8 b1)
(on b9 b2)
(on b10 b9)
(on b12 b5))
)
)


