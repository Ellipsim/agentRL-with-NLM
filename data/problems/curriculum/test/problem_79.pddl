

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b5)
(on b2 b3)
(on-table b3)
(on b4 b8)
(on-table b5)
(on-table b6)
(on b7 b2)
(on b8 b6)
(on b9 b10)
(on b10 b4)
(clear b1)
(clear b7)
(clear b9)
)
(:goal
(and
(on b1 b3)
(on b2 b5)
(on b3 b4)
(on b5 b1)
(on b7 b8)
(on b8 b2)
(on b9 b6))
)
)


