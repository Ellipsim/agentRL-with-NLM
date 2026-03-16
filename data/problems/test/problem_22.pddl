

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b8)
(on b3 b1)
(on b4 b6)
(on b5 b2)
(ontable b6)
(on b7 b3)
(on b8 b4)
(on b9 b10)
(ontable b10)
(clear b7)
(clear b9)
)
(:goal
(and
(on b2 b7)
(on b4 b8)
(on b5 b1)
(on b7 b4)
(on b8 b3)
(on b10 b5))
)
)


