

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(on b2 b6)
(ontable b3)
(on b4 b9)
(ontable b5)
(on b6 b7)
(on b7 b5)
(ontable b8)
(ontable b9)
(on b10 b2)
(clear b1)
(clear b3)
(clear b4)
(clear b8)
(clear b10)
)
(:goal
(and
(on b1 b10)
(on b3 b1)
(on b4 b2)
(on b6 b7)
(on b8 b3)
(on b9 b4)
(on b10 b6))
)
)


