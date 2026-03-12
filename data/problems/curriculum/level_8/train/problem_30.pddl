

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on-table b1)
(on b2 b5)
(on b3 b10)
(on b4 b1)
(on b5 b6)
(on-table b6)
(on-table b7)
(on-table b8)
(on b9 b2)
(on b10 b4)
(clear b3)
(clear b7)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b5)
(on b2 b4)
(on b4 b10)
(on b5 b9)
(on b6 b8)
(on b10 b6))
)
)


