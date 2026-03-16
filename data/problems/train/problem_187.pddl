

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b9)
(on b3 b5)
(on b4 b10)
(ontable b5)
(on b6 b8)
(on b7 b6)
(ontable b8)
(on b9 b3)
(ontable b10)
(clear b1)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b9)
(on b2 b4)
(on b3 b5)
(on b6 b1)
(on b7 b8)
(on b8 b3)
(on b9 b2)
(on b10 b6))
)
)


