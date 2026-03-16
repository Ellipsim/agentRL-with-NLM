

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(on b2 b6)
(ontable b3)
(on b4 b9)
(on b5 b7)
(on b6 b3)
(on b7 b1)
(ontable b8)
(on b9 b10)
(on b10 b5)
(clear b2)
(clear b4)
(clear b8)
)
(:goal
(and
(on b2 b7)
(on b3 b5)
(on b5 b2)
(on b7 b9)
(on b8 b10)
(on b9 b8)
(on b10 b1))
)
)


